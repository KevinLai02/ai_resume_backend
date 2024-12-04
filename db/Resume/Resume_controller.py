from flask import Flask, request, jsonify, g
from langchain_community.document_loaders import PyPDFLoader
from utils.AI_Model import alpaca

def resume():
    data = request.get_json()
    profession = data.get("profession")
    talent = data.get("talent")
    category = data.get("category")
    workExperience = data.get("workExperience")

    introductionRes = alpaca("用 [繁體中文] 生成一段大約150字有關 ["+ profession + "," + talent + "," + category + "] 的中文履歷自我介紹句子")
    workExperienceRes = alpaca("用繁體中文將以下這段在其他" + category + "公司的工作經驗以條列式補足300字，不要加任何標題 [" + workExperience + "]")
    talentRes = alpaca("使用者本身會[" + talent + "]這些專業技能，用繁體中文將他的專業技能敘述補足400字，不要引入任何標題 ")
    return jsonify({"introduction": introductionRes, "workExperience": workExperienceRes, "talent": talentRes})
