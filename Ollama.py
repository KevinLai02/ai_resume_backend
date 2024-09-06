import ollama
import requests
import json

def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")
        return None
    
def get_latest_user_message(data, name):
    for user in data["users"]:
        if user["name"] == name:
            return user["message"][-1]  # 最後一個 message
    return None
    



# Ollama------------------------------------------------------
# 逐行顯示
def chunk(stream):
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

def ollamaChat():
    # 限制為五次對話
    for i in range(0,5):
        #input()是python在terminal輸入的功能，str()是改成字串
        userinput = str(input())
        print(f'對話{i}')
        stream = ollama.chat(
            model='llama3.1',
            #content才是對話的輸入要放的地方
            messages=[{'role': 'user', 'content': f'{userinput}'}],
            stream=True,
        )
        chunk(stream)

# Ollama------------------------------------------------------

if __name__ == "__main__":
    api_url = 'http://127.0.0.1:8080/resume'
    data = fetch_data_from_api(api_url)
    name = "Micky"
    latest_message = get_latest_user_message(data, name)
    print(f"{name} 的最新訊息：{latest_message}")

