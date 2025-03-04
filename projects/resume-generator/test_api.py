import requests
import json

def test_deepseek_api(api_key):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 检查HTTP响应状态码
        try:
            response_data = response.json()
            print("API 响应成功：")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("响应解析失败：无法解析JSON响应。")
            print("响应内容：", response.text)
    except requests.exceptions.RequestException as e:
        print("请求失败：", e)

# 使用您的API密钥调用测试函数
api_key = "your-api-key" # 请替换为您的API密钥
test_deepseek_api(api_key)

