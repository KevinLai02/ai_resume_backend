from flask import Flask, request, jsonify, g
from ctransformers import AutoModelForCausalLM
from flask_cors import CORS
import json
from LLM.LangChainOllama import Initialize_LLM, chatLLM, rateLLM, resumeLLM
from langchain_community.document_loaders import PyPDFLoader
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Chinese-Alpaca-2-13B-GGUF",
      model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
      model_type="alpaca"
    )

app = Flask(__name__)

@app.before_request
def before_request():
    if not hasattr(g, 'chatmodel'):
        LLM = Initialize_LLM()
        g.chatmodel = LLM[0]
        g.retriever = LLM[1]

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# 音檔處理路由
@app.route("/api/process-text", methods=['POST'])
def process_text():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400
    
    return jsonify({"status": "success", "text": text})

@app.route("/AIspeak/resumeData", methods=["POST"])
def ask_resume():
    if request.method == 'POST':
        data = request.get_json()
        # save_directory = './json'
        # if not os.path.exists(save_directory):
        #     os.makedirs(save_directory)
        # filename = f"{uuid.uuid4()}.json"
        # filepath = os.path.join(save_directory, filename)
        EducationalQualifications = data.get("EducationalQualifications")
        WorkExperience = data.get("WorkExperience")
        ProfessionalSkills = data.get("ProfessionalSkills")
        TechnicalField = data.get("TechnicalField")
        resumeAutobiography = data.get("resumeAutobiography")
        Question = f"""
        此人的學歷為:{EducationalQualifications},
        工作經歷為:{WorkExperience},
        專業技能為{ProfessionalSkills},
        技術領域為:{TechnicalField},
        自傳為:{resumeAutobiography}。
        請根據上文提供的資料問1個問題
        """
        llmAnwser = []

        for i in range(5):
            llmAnwser.append(chatLLM(Question,g.chatmodel,g.retriever))
        print(llmAnwser)
        
        return jsonify({"status": "success", "llmAnwser": llmAnwser}), 200
        
    else:
        return jsonify({"message": "No data structure available to update"}), 404

@app.route("/resume", methods=['POST'])
def resume():
    data = request.get_json()
    profession = data.get("profession")
    talent = data.get("talent")
    category = data.get("category")
    workExperience = data.get("workExperience")

    introductionRes = llm("用 [繁體中文] 生成一段大約150字有關 ["+ profession + "," + talent + "," + category + "] 的中文履歷自我介紹句子")
    workExperienceRes = llm("用繁體中文將以下這段在其他" + category + "公司的工作經驗以條列式補足300字，不要加任何標題 [" + workExperience + "]")
    talentRes = llm("使用者本身會[" + talent + "]這些專業技能，用繁體中文將他的專業技能敘述補足400字，不要引入任何標題 ")
    return jsonify({"introduction": introductionRes, "workExperience": workExperienceRes, "talent": talentRes})

    
@app.route("/AIspeak/rateAnwser", methods=["POST"])
def rate_anwser():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        
        Question = f"{data},請根據資料評分"

        
        RateAnwser = rateLLM(Question,g.chatmodel)
        
        return jsonify({"status": "success", "RateAnwser": RateAnwser}), 200
        
    else:
        return jsonify({"message": "No data structure available to update"}), 404

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "key name need to be 'file' "}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    # 保存文件到指定路徑，例如 "uploads" 資料夾中
    file.save(f"./pdf/{file.filename}")
    
    ask = ["學歷","工作經歷","專業技能","技術領域","自傳"]
    pdfloader = PyPDFLoader(f"./pdf/{file.filename}")
    pages = pdfloader.load()
    col = []

    for item in ask:
        Question = f"{pages[0].page_content},你可以幫我找出此人的{item}嗎?"
        # llmAnwser.append(item)
        llmAnwser.append(resumeLLM(Question, g.chatmodel))

    EducationalQualifications = col[0]
    WorkExperience = col[1]
    ProfessionalSkills = col[2]
    TechnicalField = col[3]
    resumeAutobiography = col[4]
    Question = f"""
    此人的學歷為:{EducationalQualifications},
    工作經歷為:{WorkExperience},
    專業技能為{ProfessionalSkills},
    技術領域為:{TechnicalField},
    自傳為:{resumeAutobiography}。
    請根據上文提供的資料問1個問題
    """
    llmAnwser = []

    for i in range(5):
        llmAnwser.append(chatLLM(Question,g.chatmodel,g.retriever))
    print(llmAnwser)
    
    return jsonify({"message": f"File '{file.filename}' uploaded successfully!", "llmAnwser": llmAnwser}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


