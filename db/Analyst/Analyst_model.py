from flask import Flask, request, jsonify
import ollama
import chromadb
import pandas as pd
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 初始化資料庫 
def setup_database():
    client = chromadb.Client()
    file_path = './db/Analyst/AI_shipping_information.json'
    documents = pd.read_json(file_path)
    collection = client.get_or_create_collection(name="demodocs")

    for index, content in documents.iterrows():
        try:
            response = ollama.embeddings(model="mxbai-embed-large", prompt=content['instruction'])
            collection.add(
                ids=[str(index)], 
                embeddings=[response["embedding"]], 
                documents=[content['output']]
            )
        except ollama._types.ResponseError as e:
            print(f"API 錯誤: {e}")
            continue
    
    return collection

# 檢查中英文字符比例
def is_chinese_input_valid(user_input):
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', user_input)
    english_chars = re.findall(r'[a-zA-Z]', user_input)

    total_chars = len(chinese_chars) + len(english_chars)
    if total_chars == 0:
        return True
    english_ratio = len(english_chars) / total_chars
    return english_ratio <= 0.7

# 處理企業分析請求
def handle_user_input(user_input, collection):
    # 生成用戶輸入的嵌入向量
    response = ollama.embeddings(prompt=user_input, model="mxbai-embed-large")
    results = collection.query(query_embeddings=[response["embedding"]], n_results=3)

    if results['documents']:
        # 使用第一個查詢結果生成第一個輸出的分析
        data = results['documents'][0]

        # 生成企業簡介 
        if user_input == "長榮海運":
            enterprise_introduce = """
                企業名稱: 長榮海運
                代表人: 張衍義
                產業類別: 儲配／運輸物流業
                資本額: 700億元(新台幣)
                員工人數: 職員有9660人、海勤有2961人，共計12621名員工。
                地址: 台北市中山區民生東路二段166號1-4樓。
                公司願景: 1.創造利潤 2.照顧員工 3.回饋社會 4.持續創新 5.誠信經營。
        """
        if user_input == "陽明海運":
            enterprise_introduce = """
                企業名稱: 陽明海運
                代表人: 蔡豐明
                產業類別: 運輸物流倉儲服務業
                資本額: 450億元(新台幣)
                員工人數: 4738名岸勤人員、1230名海勤人員,共計有5968名員工
                地址: 基隆市七堵區明德一路271號。
                公司願景: 成為卓越的運輸集團，致力於提供高品質的運輸服務以滿足客戶需求。
        """
            
        if user_input == "萬海航運":
            enterprise_introduce = """
                企業名稱: 萬海航運
                代表人: 陳柏廷
                產業類別: 航海運輸服務業
                資本額: 360億元(新台幣)
                員工人數: 總員工人數為5,025人,包含3,258名海勤人員,以及1,767名海勤人員。
                地址: 台北市中山區松江路136號10樓
                公司願景: 致力於成為全球最值得信賴的運輸公司,提供高效、安全和環保的航運解決方案,並積極履行企業社會責任,為全球貿易與經濟發展貢獻力量。
        """

        # 生成企業分析
        expand_response = ollama.generate(
            model="ycchen/breeze-7b-instruct-v1_0",
            prompt=f"你是位針對{user_input}的企業分析師，請使用以下資料{data}對{user_input}進行企業分析(SWOT分析)\n\n，請用繁體中文回答問題，並請將每個部分進行分段，標題不要有缺失，且不要有數字編號。"

        )
        swot_analysis = expand_response['response']
        
        # 生成自我介紹
        introduction_response = ollama.generate(
            model="ycchen/breeze-7b-instruct-v1_0",
            prompt=f"你是位海運業的面試官，請使用以下資料對面試者進行一個自我介紹的建議(須包含讓求職者介紹個人經歷、與{user_input}類別相關的經驗、自身優勢)，並在最後給予一個範例，若需使用到名稱，請以(xxx)取代:\n\n"
                    f"{data}\n\n請用繁體中文回答問題，並請將每個部分進行分段。"
        )
        self_introduction = introduction_response['response']

        return {
            "enterprise_introduce":enterprise_introduce,
            "swot_analysis": swot_analysis,
            "self_introduction": self_introduction 
        }

    else:
        return "沒有找到相關的回答。"