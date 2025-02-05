import wechatsogou
import requests
from bs4 import BeautifulSoup
import os

# 初始化 API
ws_api = wechatsogou.WechatSogouAPI()

# 获取公众号信息
gzh_info = ws_api.get_gzh_info('企鹅吃喝指南')

# 获取公众号的文章列表
articles = ws_api.get_gzh_article_by_history('企鹅吃喝指南')

# 创建保存文章的目录
if not os.path.exists('articles'):
    os.makedirs('articles')

# 遍历文章列表并保存为纯文本
for article in articles['article']:
    title = article['title']
    content_url = article['content_url']
    
    # 获取文章内容
    response = requests.get(content_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取文章正文
    content = soup.find('div', class_='rich_media_content').get_text()
    
    # 保存为纯文本文件
    with open(f'articles/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Saved: {title}.txt')

print('All articles have been saved.')