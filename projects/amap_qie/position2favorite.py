import requests
import time
import logging
from typing import List, Dict, Optional

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="amap_favorite.log",
)
logger = logging.getLogger(__name__)

# 高德地图API Key
api_key = "1e99ffa5bc7a20c2f34c705354b61c98"  # 替换为你的高德API Key

# 地点列表（名称、地址、经纬度）
locations = [
    {"name": "惠食佳(东方大厦)", "address": "漕溪北路上实大厦五楼(徐家汇地铁站8号口旁)", "location": "121.437771,31.192640"},
    {"name": "勝记广州大排档", "address": "宁夏路236弄2号(曹杨路地铁站2号口步行400米)", "location": "121.419081,31.234323"},
    {"name": "潮人姐妹轩", "address": "海宁路269号森林湾大厦B座一楼", "location": "121.487621,31.250998"},
    {"name": "阿文潮汕食府(平型关路店)", "address": "[]", "location": "121.466788,31.268652"},
    {"name": "渔哥(龙华会店)", "address": "龙华路2778号龙华会3幢C3地上2层C3-L2S03室(龙华地铁站5号口步行80米)", "location": "121.453900,31.173423"},
    {"name": "潮凤", "address": "顶宫新路129号", "location": "117.009409,23.677194"},
    {"name": "港季茶餐厅", "address": "南京西路688号(南京西路地铁站5号口步行380米)", "location": "121.464374,31.231598"},
    {"name": "威皇", "address": "上海荟聚", "location": "121.356816,31.221773"},
    {"name": "煲山海", "address": "浦东南路2266号逸扉酒店一楼", "location": "121.513200,31.203871"},
    {"name": "小粤楼(万辉国际广场1号楼店)", "address": "万辉国际广场1号楼2层201-205室", "location": "121.422407,31.124198"},
    {"name": "盈田盈粥庄(上南路店)", "address": "上南路3077-3079号(近杨思路)", "location": "121.498217,31.161053"},
    {"name": "升记猪杂粥觅味馆(上海店)", "address": "昭化路505号昭化园103", "location": "121.422255,31.211484"},
    {"name": "陶香煲仔饭", "address": "斜土东路176号昂云空间1楼110", "location": "121.488526,31.207815"},
    {"name": "刘堡路", "address": "大兴区", "location": "116.468188,39.652765"},
    {"name": "厦门亚英餐厅(兰溪路店)", "address": "兰溪路433号(铜川路地铁站2号口步行490米)", "location": "121.401856,31.249683"},
    {"name": "临家闽南宴(正大广场店)", "address": "陆家嘴西路168号正大广场7F", "location": "121.498095,31.236587"},
    {"name": "闽和南(厦门万象城店)", "address": "禾祥东路万象城3楼328商铺", "location": "118.111889,24.471590"},
    {"name": "吴记鲜定味(吴中路店)", "address": "吴中路1050号(莲花路口北面)盛世莲花广场东楼1层", "location": "121.387619,31.178977"},
    {"name": "海上小喔(上海陆家嘴店)", "address": "崂山路707号(浦东陆家嘴金融贸易区)", "location": "121.525304,31.220228"},
    {"name": "枫林亭新浙菜(龙湖上海华泾天街店)", "address": "龙吴路2439号龙湖上海华泾天街B1层", "location": "121.455513,31.119416"},
    {"name": "闽馨风味馆", "address": "莘庄镇水清路1460弄4号101-1", "location": "121.372752,31.133075"},
    {"name": "竹屋川菜馆(淮海中路店)", "address": "淮海中路99号B107(大世界地铁站3号口步行260米)", "location": "121.478299,31.224441"},
    {"name": "本来川菜(西岸凤巢店)", "address": "云锦路683号西岸凤巢AI PLAZA北区5F层", "location": "121.460380,31.163943"},
    {"name": "花园鱼庄(丰庄店)", "address": "曹安公路1611号丰庄茶城F1层", "location": "121.367139,31.251887"},
    {"name": "赣江邨", "address": "迎轩路61号", "location": "121.317749,31.004805"},
    {"name": "大上饶饶帮菜", "address": "凤凰大道99号7栋107、207", "location": "117.982188,28.462443"},
    {"name": "江西客家传统小炒(福山路店)", "address": "商城路1118号", "location": "121.526930,31.234141"},
    {"name": "谭姐湘菜馆(浦东大道店)", "address": "浦东大道1028号(源深路地铁站3A口步行120米)", "location": "121.532395,31.241435"},
    {"name": "湘润土菜馆(广灵二路商业街店)", "address": "广灵二路341号", "location": "121.472324,31.283640"},
    {"name": "柒货土菜供销社", "address": "曹安公路2076号(嘉怡路地铁站1号口步行210米)", "location": "121.348205,31.258958"},
    {"name": "湘椒(鸿寿坊店)", "address": "西康路1117号1-2层(长寿路地铁站3号口步行240米)", "location": "121.440473,31.241363"},
    {"name": "菁菁有味恩施菜馆(禹洲·金桥国际3期店)", "address": "金湘路199号禹洲·金桥国际3期F1层", "location": "121.612523,31.255573"},
    {"name": "泓0871臻选云南菜(上海北外滩店)", "address": "吴淞路130号城投控股大厦副楼彩虹北F5层", "location": "121.490448,31.247023"},
    {"name": "云味·大可堂", "address": "陕西南路548号乙(近绍兴路)", "location": "121.461568,31.207945"},
    {"name": "傣着园", "address": "亭林镇复兴东路59号102室", "location": "121.317942,30.881154"},
    {"name": "源禾清小馆", "address": "中漕路98号(近华亭宾馆)", "location": "121.433440,31.183156"},
    {"name": "荣季95·小海鲜酒馆", "address": "虎丘路28号1F(南京东路地铁站6号口步行480米)", "location": "121.487460,31.241650"},
    {"name": "绍兴名菜馆(可乐路店)", "address": "可乐路238-240号", "location": "121.363123,31.206451"},
    {"name": "温州牛肉馆(石泉秋月枫舍步行街店)", "address": "中山北路2139弄22-1号石泉秋月枫舍步行街", "location": "121.428734,31.247710"},
    {"name": "清江佬海鲜面(丰庄路店)", "address": "新郁支路丰庄路交差口", "location": "121.366051,31.251452"},
    {"name": "老村庄野鱼馆(曲阳路店)", "address": "腾克路120号二楼(近曲阳路)", "location": "121.491412,31.290854"},
    {"name": "南陵人家·经典土菜", "address": "凯旋路901号(延安西路地铁站2号口步行480米)", "location": "121.417171,31.205886"},
    {"name": "席家花园(巨鹿花园店)", "address": "巨鹿路889号距地铁14号线静安寺站11号口步行990m", "location": "121.448300,31.217658"},
    {"name": "豪生酒家", "address": "广元路156-1号", "location": "121.439812,31.199198"},
    {"name": "半盆菜酒家", "address": "中山南一路893号(近鲁班路口)", "location": "121.476133,31.197216"},
    {"name": "玮丰酒家(南昌路178弄小区店)", "address": "南昌路188号(淮海中路地铁站1号口步行290米)", "location": "121.466404,31.218326"},
    {"name": "157食坊(上海凯旋商务中心店)", "address": "凯旋路1406号(近虹桥路地铁站)", "location": "121.419879,31.200509"},
    {"name": "二雷吉林烧烤(灵石路旗舰店)", "address": "灵石路699号", "location": "121.445019,31.283168"},
    {"name": "老胖烧烤吉林小串(河间路店)", "address": "河间路810号", "location": "121.542926,31.271020"},
    {"name": "胜彪餐饮店(航北路店)", "address": "航北路15号", "location": "121.359408,31.174583"}
]

# 创建收藏夹
def create_favorite_folder(api_key: str, folder_name: str, retries: int = 3) -> Optional[str]:
    url = "https://restapi.amap.com/v3/favorite/create"
    params = {
        "key": api_key,
        "name": folder_name,
        "type": "1"  # 1表示收藏夹
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            if data.get("status") == "1":
                logger.info(f"收藏夹创建成功，ID：{data['data']['id']}")
                return data["data"]["id"]  # 返回收藏夹ID
            else:
                error_info = data.get("info", "未知错误")
                logger.error(f"收藏夹创建失败，错误信息：{error_info}")
                if attempt < retries - 1:
                    time.sleep(2)  # 重试前等待2秒
                    continue
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败：{e}")
            if attempt < retries - 1:
                time.sleep(2)  # 重试前等待2秒
                continue
            return None
    return None

# 添加地点到收藏夹
def add_to_favorite(api_key: str, folder_id: str, name: str, address: str, location: str, retries: int = 3) -> bool:
    url = "https://restapi.amap.com/v3/favorite/add"
    params = {
        "key": api_key,
        "folderid": folder_id,
        "name": name,
        "address": address,
        "location": location
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            if data.get("status") == "1":
                logger.info(f"地点添加成功：{name}")
                return True  # 添加成功
            else:
                error_info = data.get("info", "未知错误")
                logger.error(f"地点添加失败：{name}，错误信息：{error_info}")
                if attempt < retries - 1:
                    time.sleep(2)  # 重试前等待2秒
                    continue
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败：{e}")
            if attempt < retries - 1:
                time.sleep(2)  # 重试前等待2秒
                continue
            return False
    return False

# 主函数
def main():
    # 创建收藏夹
    folder_name = "企鹅吃喝指南"
    logger.info(f"正在创建收藏夹：{folder_name}")
    folder_id = create_favorite_folder(api_key, folder_name)
    if not folder_id:
        logger.error("收藏夹创建失败，程序退出。")
        return

    print(f"收藏夹创建成功，ID：{folder_id}")

    # 将地点添加到收藏夹
    logger.info("开始添加地点到收藏夹...")
    for location in locations:
        success = add_to_favorite(api_key, folder_id, location["name"], location["address"], location["location"])
        if success:
            print(f"已添加：{location['name']}")
        else:
            print(f"添加失败：{location['name']}")
        time.sleep(1)  # 添加延时，避免触发API频率限制

    # 获取收藏夹 URL
    favorite_url = f"https://m.amap.com/favorite/detail/{folder_id}"
    print(f"\n收藏夹 URL: {favorite_url}")
    logger.info(f"收藏夹 URL: {favorite_url}")

if __name__ == "__main__":
    main()