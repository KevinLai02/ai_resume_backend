from flask import Flask, jsonify    
from ctransformers import AutoModelForCausalLM
from flask_cors import CORS

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Chinese-Alpaca-2-13B-GGUF",
      model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
      model_type="alpaca"
    )

app = Flask(__name__)
CORS(app)
@app.route("/resume", methods=['GET'])
def resume():
    res = llm("用 [中文] 生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子")
    return jsonify({"message": res}) 
    # return jsonify({"message": 'hello world'}) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)