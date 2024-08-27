from flask import Flask, request, jsonify
from ctransformers import AutoModelForCausalLM
from flask_cors import CORS
import json

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# llm = AutoModelForCausalLM.from_pretrained(
#     "TheBloke/Chinese-Alpaca-2-13B-GGUF",
#       model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
#       model_type="alpaca"
#     )

# 讀取 JSON 檔案
def load_users():
    with open("./json/users.json", "r", encoding="utf-8") as file:
        return json.load(file)
def load_resumeData():
    with open("./json/resumeData.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_users(users):
    with open("./json/users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)
def save_resumeData(data_storage):
    with open("./json/resumeData.json", "w", encoding="utf-8") as file:
        json.dump(data_storage, file, ensure_ascii=False, indent=4)

# 加載JSON檔
users = load_users()
# print(users)
data_storage = load_resumeData()

# data_storage = [
#     {
#         "resumeData":[
#             {
#                 "resumeName":"",
#                 "resumeField1":"",
#                 "resumeField2":"",
#                 "resumeField3":"",
#                 "resumeAutobiography":""
#             }
#         ]
#     }
# ]

app = Flask(__name__)
CORS(app)
# @app.route("/resume", methods=['GET'])
# def resume():
#     res = llm("用 [中文] 生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子")
#     return jsonify({"message": res}) 
#     你這裡的問題應該是要返回json檔res不是json所以不行
#     # return jsonify({"message": 'hello world'}) 

# ------------------Kevin前端JSON 欄位資料------------------------------
@app.route("/resumeData", methods=["GET"])
def get_resumeData():
    if not data_storage:
        return jsonify({"message": "No data available"}), 404
    return jsonify(data_storage), 200

@app.route("/resumeData", methods=["POST"])
def add_resume():
    new_data = request.json

    # 確保有數據可以填充
    if not data_storage or not data_storage[0].get("resumeData"):
        return jsonify({"message": "No data structure available to update"}), 404

    # 填充數據到第一個resumeData結構中
    resume = data_storage[0]["resumeData"][0]

    resume["resumeName"] = new_data.get("resumeName", resume["resumeName"])
    resume["resumeField1"] = new_data.get("resumeField1", resume["resumeField1"])
    resume["resumeField2"] = new_data.get("resumeField2", resume["resumeField2"])
    resume["resumeField3"] = new_data.get("resumeField3", resume["resumeField3"])
    resume["resumeAutobiography"] = new_data.get("resumeAutobiography", resume["resumeAutobiography"])
    save_resumeData(data_storage)
    return jsonify({"message": "Data updated successfully"}), 200

# @app.route('/resumeData', methods=['DELETE'])
# def delete_resume():
#     if not data_storage:
#         return jsonify({"message": "No data to clear"}), 404

#     for item in data_storage:
#         for resume in item.get("resumeData", []):
#             resume["resumeName"] = ""
#             resume["resumeField1"] = ""
#             resume["resumeField2"] = ""
#             resume["resumeField3"] = ""
#             resume["resumeAutobiography"] = ""

#     return jsonify({"message": "Data deleted successfully"}), 200

# -----------------------------------------------------------------

# 獲取所有用戶的信息
@app.route("/resume", methods=["GET"])
def get_user():
    return jsonify({"users": users})

# 創建新的用戶
@app.route("/resume", methods=["POST"])
def create_user():
    request_data = request.get_json()
    new_user = {"name": request_data["name"], "message": [], "llm_anwser": []}
    users.append(new_user)
    save_users(users)  # 保存到 JSON 檔案
    return jsonify(new_user), 201

# 在指定用戶中添加訊息
@app.route("/resume/<string:name>/message", methods=["POST"])
def add_message_to_user(name):
    request_data = request.get_json()
    for user in users:
        if user["name"] == name:
            new_message = request_data["message"]
            user["message"].append(new_message)
            save_users(users)  # 保存到 JSON 檔案
            return jsonify({"message": f"Course {new_message} added to user {name}"}), 201
    return jsonify({"message": "usesr not found"}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)