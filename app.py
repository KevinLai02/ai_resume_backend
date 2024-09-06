from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from ctransformers import AutoModelForCausalLM
from flask_cors import CORS

llm = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Chinese-Alpaca-2-13B-GGUF",
    model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
    model_type="alpaca"
)

app = Flask(__name__)

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

# 生成履歷文本路由
@app.route("/resume", methods=['GET'])
def resume():
    res = llm("用 [中文] 生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子")
    return jsonify({"message": res})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

