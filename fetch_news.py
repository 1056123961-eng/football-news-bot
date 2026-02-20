import requests
import json
import os
from datetime import datetime

def fetch():
    api_key = os.environ.get("TIAN_API_KEY")
    # 使用你申请的“体育新闻”接口地址
    url = f"https://apis.tianapi.com/tiyu/index?key={api_key}&num=1000"
    
    try:
        response = requests.get(url)
        res = response.json()
        
        if res.get("code") == 200:
            all_news = res["result"]["newslist"]
            
            # --- 曼联新闻筛选逻辑 ---
            # 只有标题或描述里包含“曼联”、“Manchester United”或“红魔”才保留
            keywords = ['曼联', '曼彻斯特联', '红魔', 'Manchester United'，“足球”]
            mu_news = []
            
            for item in all_news:
                # 检查标题或简述是否命中关键词
                text_to_check = (item['title'] + item['description']).lower()
                if any(k in text_to_check for k in keywords):
                    
                    # 结合 119 版本的高位派发/热点识别逻辑
                    title = item['title']
                    if any(kw in title for kw in ['官宣', 'Here we go', '达成协议']):
                        item['display_tag'] = "🔥重磅"
                    elif any(kw in title for kw in ['转会', '报价', '挖角']):
                        item['display_tag'] = "🚨头条"
                    else:
                        item['display_tag'] = "资讯"
                        
                    mu_news.append(item)
            
            # 封装数据
            output = {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "count": len(mu_news),
                "data": mu_news
            }
            
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            
            print(f"成功筛选出 {len(mu_news)} 条曼联新闻")
            
        else:
            print(f"API报错: {res.get('msg')}")
            
    except Exception as e:
        print(f"脚本执行错误: {e}")

if __name__ == "__main__":
    fetch()
