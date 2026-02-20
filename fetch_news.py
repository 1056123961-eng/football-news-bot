import requests
import json
import os
from datetime import datetime

def fetch():
    api_key = os.environ.get("TIAN_API_KEY")
    # 调试：打印 Key 的前几位（不要全打印，安全第一）
    if api_key:
        print(f"API Key found, starts with: {api_key[:5]}...")
    else:
        print("Error: TIAN_API_KEY not found in environment!")
        return

    url = f"https://apis.tianapi.com/worldsoccer/index?key={api_key}&num=30"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        res = response.json()
        print(f"API Response Code: {res.get('code')}")
        
        if res.get("code") == 200:
            news_list = res["result"]["newslist"]
            for item in news_list:
                title = item['title']
                if any(kw in title for kw in ['官宣', '达成协议', 'Here we go']):
                    item['display_tag'] = "🔥重磅"
                elif any(kw in title for kw in ['亿元', '破纪录', '千万欧']):
                    item['display_tag'] = "🚨头条"
                else:
                    item['display_tag'] = "资讯"
            
            output = {"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": news_list}
            # 确保文件被写入
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print("Successfully created news.json")
        else:
            print(f"API Error Message: {res.get('msg')}")
            # 如果接口报错，我们也生成一个空文件，防止 Git 报错中止
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump({"error": "api_error", "msg": res.get('msg')}, f)

    except Exception as e:
        print(f"Python Script Error: {e}")
        # 出错也生成一个文件，保证 Workflow 能跑完
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f)

if __name__ == "__main__":
    fetch()
