import requests
import json
import os
from datetime import datetime

def fetch():
    api_key = os.environ.get("TIAN_API_KEY")
    # 请求 5000 条体育新闻，扩大基数
    url = f"https://apis.tianapi.com/tiyu/index?key={api_key}&num=5000"
    
    try:
        response = requests.get(url)
        res = response.json()
        
        if res.get("code") == 200:
            all_news = res["result"]["newslist"]
            
            mu_keywords = ['曼联', '红魔', 'Man Utd', 'Manchester United', '阿莫林', 'B费']
            soccer_keywords = ['足球', '英超', '欧冠', '西甲', '意甲', '德甲', '转会', '豪门']
            
            final_list = []
            
            for item in all_news:
                full_text = (item['title'] + item['description']).lower()
                
                # 1. 如果是曼联新闻，打上最高级标签，放入列表
                if any(k.lower() in full_text for k in mu_keywords):
                    item['display_tag'] = "🔥重磅"
                    # 给曼联新闻一个权重排序分
                    item['priority'] = 1 
                    final_list.append(item)
                
                # 2. 如果不是曼联但含有足球关键词，也保留作为内容填充
                elif any(k in full_text for k in soccer_keywords):
                    item['display_tag'] = "资讯"
                    item['priority'] = 2
                    final_list.append(item)
            
            # 按优先级排序：曼联永远在最上面
            final_list.sort(key=lambda x: x.get('priority', 9))

            output = {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "count": len(final_list),
                "data": final_list
            }
            
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            
            print(f"同步完成，共抓取 {len(final_list)} 条足球/曼联动态")
        else:
            print(f"API Error: {res.get('msg')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch()
