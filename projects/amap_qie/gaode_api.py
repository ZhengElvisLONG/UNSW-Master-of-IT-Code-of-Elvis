import requests
import json  # 导入 json 模块

# 高德地图API Key
api_key = "1e99ffa5bc7a20c2f34c705354b61c98"  # 替换为你的 API Key

# 餐厅列表
restaurants = [
    "惠食佳", "胜记大排档", "潮人姐妹轩", "阿文潮汕食府", "甘草潮夜档", 
    "渔哥·湛江", "潮凤", "港季", "南北湘", "威皇", "煲山海", "小粤楼", 
    "33度·新季港式烧鹅王", "盈田盈粥庄", "升记", "陶香煲仔饭", "佳记", 
    "刘卜", "亚英餐厅", "临家·闽南宴", "闽和南·欢宴", "吴记鲜定味", 
    "海上家眷", "台南担仔面", "龙岩菜", "闽馨风味馆", "老吴家川菜", 
    "竹屋", "本来川菜", "花园鱼庄", "觉味燃面", "赣江村", "饶帮菜", 
    "江西客家传统小炒", "芥菜园", "谭姐湘菜馆", "湘润土菜馆", 
    "柒货·土菜供销社", "湘御", "湘椒", "菁菁有味", "泓0871臻选云南菜", 
    "刘和园", "边陲傣家", "云味", "傣着园", "跳河大排档", "桂林板路", 
    "源禾清小馆", "荣季95", "绍兴名菜馆", "温州海鲜黄牛馆", 
    "温州牛肉馆（镇坪路）", "清江佬海鲜面", "老村庄野鱼馆", 
    "淮扬韵·淮阳味道", "南陵人家", "席家花园", "豪生酒家", "珊岛", 
    "半盆菜酒家", "玮丰酒家", "157食坊", "胶东渔村", "青岛海鲜", 
    "二雷吉林烧烤", "老胖吉林小串烧烤", "胜彪烧烤店", "小木屋米酒吧", 
    "八仙黑驴肉馆"
]

# 存储查询结果
results = []

# 计数器
found_count = 0  # 找到的餐厅数量
not_found_count = 0  # 未找到的餐厅数量

# 查询每个餐厅的地址
for restaurant in restaurants:
    found = False  # 标记是否找到结果

    # 方式 1：严格匹配（城市范围内搜索）
    url = f"https://restapi.amap.com/v3/place/text?key={api_key}&keywords={restaurant}&city=上海&offset=1&page=1"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1" and int(data["count"]) > 0:
        poi = data["pois"][0]  # 只取第一个匹配结果
        name = poi["name"]
        address = poi["address"]
        location = poi["location"]  # 经纬度
        results.append({"name": name, "address": address, "location": location})
        found = True
        found_count += 1
    else:
        print(f"方式 1 未找到餐厅：{restaurant}")

    # 方式 2：放宽城市限制（全国范围内搜索）
    if not found:
        url = f"https://restapi.amap.com/v3/place/text?key={api_key}&keywords={restaurant}&offset=1&page=1"
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "1" and int(data["count"]) > 0:
            poi = data["pois"][0]  # 只取第一个匹配结果
            name = poi["name"]
            address = poi["address"]
            location = poi["location"]  # 经纬度
            results.append({"name": name, "address": address, "location": location})
            found = True
            found_count += 1
        else:
            print(f"方式 2 未找到餐厅：{restaurant}")

    # 方式 3：增加关键词灵活性（餐厅名称 + 上海）
    if not found:
        url = f"https://restapi.amap.com/v3/place/text?key={api_key}&keywords={restaurant} 上海&offset=1&page=1"
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "1" and int(data["count"]) > 0:
            poi = data["pois"][0]  # 只取第一个匹配结果
            name = poi["name"]
            address = poi["address"]
            location = poi["location"]  # 经纬度
            results.append({"name": name, "address": address, "location": location})
            found = True
            found_count += 1
        else:
            print(f"方式 3 未找到餐厅：{restaurant}")

    # 如果仍未找到，记录未找到的餐厅
    if not found:
        results.append({"name": restaurant, "address": "未找到", "location": "未找到"})
        not_found_count += 1

# 打印结果
for result in results:
    print(f"{result['name']} - {result['address']} - {result['location']}")

# 打印统计结果
print(f"\n总计：找到 {found_count} 家餐厅，未找到 {not_found_count} 家餐厅。")

# 保存 results 到文件
with open("restaurants_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
print("\n餐厅结果已保存到 restaurants_results.json 文件中。")

# 创建收藏夹并添加地点
def create_favorite_folder(api_key, folder_name):
    url = "https://restapi.amap.com/v3/favorite/create"
    params = {
        "key": api_key,
        "name": folder_name,
        "type": "1"  # 1表示收藏夹
    }
    response = requests.post(url, params=params)
    return response.json()

def add_to_favorite(api_key, folder_id, name, address, location):
    url = "https://restapi.amap.com/v3/favorite/add"
    params = {
        "key": api_key,
        "folderid": folder_id,
        "name": name,
        "address": address,
        "location": location
    }
    response = requests.post(url, params=params)
    return response.json()

# 创建收藏夹
folder_name = "企鹅吃喝指南"
folder_response = create_favorite_folder(api_key, folder_name)
if folder_response["status"] == "1":
    folder_id = folder_response["data"]["id"]
    print(f"收藏夹创建成功，ID：{folder_id}")
else:
    print("收藏夹创建失败")
    exit()

# 将查询到的地点添加到收藏夹
for result in results:
    if result["address"] != "未找到":  # 只添加找到的餐厅
        add_response = add_to_favorite(api_key, folder_id, result["name"], result["address"], result["location"])
        if add_response["status"] == "1":
            print(f"已添加：{result['name']}")
        else:
            print(f"添加失败：{result['name']}")

# 获取收藏夹 URL
favorite_url = f"https://m.amap.com/favorite/detail/{folder_id}"
print(f"\n收藏夹 URL: {favorite_url}")