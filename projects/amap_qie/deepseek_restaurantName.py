import requests
import json

# DeepSeek API 的 URL 和你的 API 密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = "sk-8071258bf06549209c7aa987f4c1d424"

# 请求头，包含 API 密钥
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 示例：从本地文件读取文章内容（假设你已经爬取了文章并保存为文本文件）
def load_article_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# 使用 DeepSeek 提取餐厅名称
def extract_restaurant_names(content):
    # 构建 Prompt
    prompt = f"""
    你是一个专业的餐厅名称提取工具。请从以下文章中提取所有提到的餐厅名称，并以 JSON 格式返回。要求：
    1. 只返回餐厅名称，不要返回其他内容。
    2. 如果文章中没有提到餐厅名称，返回空列表。
    3. 餐厅名称必须完整且准确。

    文章内容：
    {content}

    返回格式：
    {{
        "restaurant_names": ["餐厅名称1", "餐厅名称2", ...]
    }}
    """

    # 调用 DeepSeek 模型
    data = {
        "model": "deepseek-chat",  # 根据实际模型名称填写
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # 解析模型返回的内容
        try:
            output = result["choices"][0]["message"]["content"]
            return json.loads(output)["restaurant_names"]
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Failed to parse model output: {e}")
            return []
    else:
        print(f"Failed to call DeepSeek API: {response.status_code}, Response: {response.text}")
        return []

# 主函数
def main():
    # 从本地文件加载文章内容（假设文件路径为 "article.txt"）
    article_content = load_article_from_file("article.txt")

    # 提取餐厅名称
    restaurant_names = extract_restaurant_names(article_content)

    # 输出结果
    print("提取到的餐厅名字：")
    for name in restaurant_names:
        print(name)

if __name__ == "__main__":
    main()