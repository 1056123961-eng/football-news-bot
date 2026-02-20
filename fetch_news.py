import requests
import json
import os
from datetime import datetime

def fetch():
    api_key = os.environ.get("TIAN_API_KEY")
    url = f"https://apis.tianapi.com/tiyu/index?key={api_key}&num=100"
    
    try:
        response = requests.get(url)
        res = response.json()
        
        if res.get("code") == 200:
            all_news = res["result"]["newslist"]
            
            mu_keywords = ['曼联', '红魔', 'Man Utd', '滕哈格', '阿莫林', 'B费', '拉什福德']
            soccer_keywords = ['足球', '英超', '欧冠', '转会', '英格兰']
            # 保底关键词：只要是体育，全都要
            insurance_keywords = ['赛', '队', '球', '战', '胜', '负']
            
            final_list = []
            
            for item in all_news:
                full_text = (item['title'] + item['description']).lower()
                
                # 判定级别
                if any(k in full_text for k in mu_keywords):
                    item['display_tag'] = "🔥重磅"
                    item['priority'] = 1
                elif any(k in full_text for k in soccer_keywords):
                    item['display_tag'] = "🚨头条"
                    item['priority'] = 2
                elif any(k in full_text for k in insurance_keywords):
                    item['display_tag'] = "资讯"
                    item['priority'] = 3
                else:
                    continue # 如果连个“赛”字都没有，才丢弃
                
                final_list.append(item)
            
            # 排序：曼联 > 足球 > 其他体育
            final_list.sort(key=lambda x: x.get('priority', 9))

            output = {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "count": len(final_list),
                "data": final_list
            }
            
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"Update Success: {len(final_list)} items found.")
        else:
            print(f"API Error: {res.get('msg')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch()
