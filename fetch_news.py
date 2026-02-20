import requests
import json
import os
from datetime import datetime

def fetch():
    api_key = os.environ.get("TIAN_API_KEY")
    url = f"https://apis.tianapi.com/worldsoccer/index?key={api_key}&num=30"
    
    try:
        response = requests.get(url)
        res = response.json()
        if res.get("code") == 200:
            news_list = res["result"]["newslist"]
            # 简单的逻辑加工
            for item in news_list:
                title = item['title']
                if any(kw in title for kw in ['官宣', '达成协议', 'Here we go']):
                    item['display_tag'] = "🔥重磅"
                elif any(kw in title for kw in ['亿元', '破纪录', '千万欧']):
                    item['display_tag'] = "🚨头条"
                else:
                    item['display_tag'] = "资讯"
            
            output = {"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": news_list}
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch()
