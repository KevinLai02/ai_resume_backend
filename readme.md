範例圖片:  
![image](https://github.com/KevinLai02/ai_resume_backend/blob/main/txt/postmanExample.png)  
  
這個是賴你用來傳資料給我  
POST http://127.0.0.1:8080/AIspeak/resumeData  
{  
    "EducationalQualifications":"大學畢業",  
    "WorkExperience":"沒有經驗",  
    "ProfessionalSkills":"擅長python程式語言",  
    "TechnicalField":"海事資訊科技系",  
    "resumeAutobiography":"我是一名大學畢業生，主修海事資訊科技系。在大學期間，我不僅掌握了該領域的  專業知識，還積極學習了Python程式語言，並在此方面展現了較強的能力。雖然我目前沒有正式的工作經驗，但在學習過程中，  我參與了多個課程專案，這些專案使我能夠將理論與實踐相結合，並進一步提高了我的技術技能。海事資訊科技是一個多元且  充滿挑戰的領域，結合了資訊技術與海事應用的知識。在學習過程中，我對相關技術和應用有了深刻的理解，並且我發現自己  對使用程式語言解決問題充滿興趣。特別是Python語言，它的靈活性和強大功能讓我能夠快速開發出解決方案，並應用於不同  的技術環境中。儘管我目前缺乏工作經驗，但我相信憑藉我對程式設計的熱忱、扎實的專業基礎以及快速學習新技能的能力，  我能夠在未來的職涯中充分發揮我的潛力。我期望能夠在工作中繼續提升自己，並為公司和團隊帶來有價值的貢獻。"  
}
![image](https://github.com/KevinLai02/ai_resume_backend/blob/main/txt/chatLLM.png)  

這是用來評分  
POST http://127.0.0.1:8080/AIspeak/rateAnwser  
{  
    "q1":"請問你是否有大學畢業的資格證明文件？",  
    "a1":"是的，我有大學畢業的資格證明文件，並可以提供相關證書作為證明。",  
    "q2":"請問你是否具有相關系科的畢業證書或認可文件？",  
    "a2":"是的，我擁有海事資訊科技系的畢業證書，並且具備相關領域的專業知識。",  
    "q3":"請問你在自傳中提到的python程式語言是否是你目前所擅長的技能？",  
    "a3":"是的，Python程式語言是我目前擅長的技能，我在學習過程中已經熟練掌握了它的應用。",  
    "q4":"請問你是否具備海事資訊科技系領域的相關技術和知識？",  
    "a4":"是的，我在海事資訊科技系的學習中掌握了相關的技術和知識，能夠應用於實際問題解決。",  
    "q5":"請問你將如何應用你的程式設計能力於未來工作的職涯中？",  
    "a5":"我計劃將我的程式設計能力應用於解決技術問題，優化工作流程，並在海事資訊科技或相關領域中開發出有效的技術解決方案，為公司帶來創新和效率"  
}  

這是用來找履歷資料會回傳陣列包含五個欄位  
POST http://127.0.0.1:8080//upload  
記得用desktop postman form data 上傳檔案  
![image](https://github.com/KevinLai02/ai_resume_backend/blob/main/txt/postman-resume.png) 