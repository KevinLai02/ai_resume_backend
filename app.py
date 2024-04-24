from flask import Flask, jsonify    
from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# llm = AutoModelForCausalLM.from_pretrained(
#     "TheBloke/Chinese-Alpaca-2-13B-GGUF",
#       model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
#       model_type="alpaca"
#     )

app = Flask(__name__)
@app.route("/resume")
def resume():
    # return jsonify({"message": llm("生成一段大約100字有關 [前端工程師，工作經歷3年] 的中文履歷自我介紹句子，不要用條列式")}) 
    return jsonify({"message": 'hello world'}) 

if __name__ == '__main__':
    app.run()