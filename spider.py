# spider.py
import requests
import pandas as pd
import time
import random
import re
import hashlib
import urllib.parse

def get_wbi_keys():
    """获取B站WBI签名所需的 img_key 和 sub_key"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/'
    }
    try:
        response = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
        data = response.json()
        wbi_img = data['data']['wbi_img']
        img_url = wbi_img['img_url']
        sub_url = wbi_img['sub_url']
        
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return img_key, sub_key
    except Exception as e:
        print(f"获取WBI密钥失败: {e}")
        return None, None

def get_mixin_key(orig):
    """WBI签名混淆算法"""
    mixin_key_enc_tab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]
    return ''.join([orig[i] for i in mixin_key_enc_tab])[:32]

def enc_wbi(params, img_key, sub_key):
    """对请求参数进行WBI签名"""
    mixin_key = get_mixin_key(img_key + sub_key)
    curr_time = int(time.time())
    params['wts'] = curr_time
    
    # 参数排序并拼接
    params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(params)
    
    # 计算w_rid
    wbi_sign = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params['w_rid'] = wbi_sign
    return params

def get_bilibili_recommend(cookie_str):
    """爬取B站首页推荐视频 (100条多页版)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Accept': 'application/json, text/plain, */*',
        'Cookie': cookie_str
    }
    
    print("正在获取WBI密钥...")
    img_key, sub_key = get_wbi_keys()
    if not img_key or not sub_key:
        print("获取WBI密钥失败，请检查网络。")
        return

    base_url = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
    video_data = []
    
    # 循环爬取 10 页，每页 20 条
    for page in range(1, 11):
        print(f"\n--- 正在爬取第 {page} 页 ---")
        
        params = {
            'web_location': 1430650,
            'y_num': 4,
            'fresh_type': 4,
            'feed_version': 'V8',
            'fresh_idx_1h': page,  
            'fetch_row': 20,
            'fresh_idx': page,     
            'brush': page,        
            'device': 'linux',
            'homepage_ver': 1,
            'ps': 20,
            'last_y_num': 5,
            'screen': '1600-1200'
        }
        
        signed_params = enc_wbi(params, img_key, sub_key)
        query_string = urllib.parse.urlencode(signed_params)
        full_url = f"{base_url}?{query_string}"
        
        try:
            response = requests.get(full_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    for item in data['data']['item']:
                        title = item.get('title', '')
                        clean_title = re.sub(r'<.*?>', '', title)
                        video_data.append({'title': clean_title})
                        print(f"获取: {clean_title}")
                else:
                    print(f"接口错误: {data['code']}，信息: {data.get('message')}")
            else:
                print(f"请求被拦截: {response.status_code}")
        except Exception as e:
            print(f"请求异常: {e}")
            
        # 爬完一页休眠 2 秒，防止被风控
        time.sleep(random.uniform(1, 3))

    # 保存数据（只保存一次，确保是100条）
    if video_data:
        df = pd.DataFrame(video_data)
        df.to_csv('bilibili_recommend.csv', index=False, encoding='utf-8-sig')
        print(f"\n数据保存成功！共爬取 {len(video_data)} 条视频数据。")
    else:
        print("未获取到数据。")

if __name__ == '__main__':
    
    # ⚠️ 请在这里填入你自己的B站Cookie
    # 获取方式：登录B站 -> F12 -> 控制台 -> 输入 document.cookie
    MY_COOKIE = "YOUR_COOKIE_HERE" 

    get_bilibili_recommend(MY_COOKIE)