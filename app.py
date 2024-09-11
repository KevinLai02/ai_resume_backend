from flask import Flask, request, jsonify, g
from ctransformers import AutoModelForCausalLM
from flask_cors import CORS
import json
from LLM.LangChainOllama import Initialize_LLM, chatLLM

# llm = AutoModelForCausalLM.from_pretrained(
#     "TheBloke/Chinese-Alpaca-2-13B-GGUF",
#     model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
#     model_type="alpaca"
# )

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

# # 生成履歷文本路由
# @app.route("/resume", methods=['GET'])
# def resume():
#     res = llm("用 [中文] 生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子")
#     return jsonify({"message": res})
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# llm = AutoModelForCausalLM.from_pretrained(
#     "TheBloke/Chinese-Alpaca-2-13B-GGUF",
#       model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
#       model_type="alpaca"
#     )
# @app.route("/resume", methods=['GET'])
# def resume():
#     res = llm("用 [中文] 生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子")
#     return jsonify({"message": res}) 
#     你這裡的問題應該是要返回json檔res不是json所以不行
#     # return jsonify({"message": 'hello world'}) 

@app.route("/AIspeak/resumeData", methods=["POST"])
def add_resume():
    if request.method == 'POST':
        data = request.get_json()
        # save_directory = './json'
        # if not os.path.exists(save_directory):
        #     os.makedirs(save_directory)
        # filename = f"{uuid.uuid4()}.json"
        # filepath = os.path.join(save_directory, filename)
        
        resumeAutobiography = data.get("resumeAutobiography")
        Question = f"{resumeAutobiography}。請根據上文問一個問題"
        
        LLManwser = chatLLM(Question,g.chatmodel,g.retriever)
        
        return jsonify({"status": "success", "LLManwser": LLManwser}), 200
        
    else:
        return jsonify({"message": "No data structure available to update"}), 404
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


