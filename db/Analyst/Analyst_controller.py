from flask import request, jsonify
from db.Analyst.Analyst_model import setup_database, handle_user_input, is_chinese_input_valid

def analyze():
    data = request.json
    print(data)
    user_input = data.get("user_input")

    if not user_input: 
        return jsonify({"error": "請輸入問題"}), 400

    if not is_chinese_input_valid(user_input):
        return jsonify({"error": "請輸入中文！"}), 400

    collection = setup_database()
    result = handle_user_input(user_input, collection)
    enterprise_introduce = result.get('enterprise_introduce')
    swot_analysis = result.get('swot_analysis')
    self_introduction = result.get('self_introduction')

    if swot_analysis and self_introduction:
        return jsonify({

            "enterprise_introduce":enterprise_introduce,
            "swot_analysis": swot_analysis,
            "self_introduction": self_introduction
        })
    else:
        return jsonify({"error": "沒有找到相關的回答。"}), 404
