import requests
from bs4 import BeautifulSoup
 
index_url = "https://api.bilibili.com/pgc/web/season/section?season_id=2660"

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
 
# 通过番剧首页获取每一话对应的cid编号，存入section_sid
def get_cid(index_url):
    try:
        index_response = requests.get(index_url, headers=header)
        index_json = index_response.json() # 返回一个json文件
        section_cid = []
         
        for each in index_json['result']['main_section']['episodes']:
            section_cid.append({
                'title': each['long_title'],
                'cid': each['cid'],
                'id': each['id'],
                'url': each['share_url']
            })
    except:
        print('index pass')
     
    return section_cid
 
# 通过cid编号获取这一话的所有弹幕信息
def get_danmu(cid):
    try:
        danmu_response = requests.get('https://api.bilibili.com/x/v1/dm/list.so?oid='+str(cid), headers=header)
        danmu_soup = BeautifulSoup(danmu_response.content)
        print('succeed')
        for each in danmu_soup.findAll('d'):
            danmu_info = each['p'].split(",")
            danmu_detail.append({
                'cid': cid, # 弹幕对应视频cid
                'danmu': each.get_text(), # 弹幕内容
                'time': danmu_info[0], # 弹幕出现时间（秒）
                'type': danmu_info[1], # 弹幕模式
                'size': danmu_info[2], # 字号
                'color': danmu_info[3], # 颜色
                'timestamp': danmu_info[4], # 时间戳
                'pool': danmu_info[5], # 弹幕池
                'sender': danmu_info[6], # 发送者ID
                'row': danmu_info[7] # 弹幕rowID，用于“历史弹幕”功能
            })
        print(cid, 'done')
    except:
        print(cid, 'pass')
 
danmu_detail = [] # 所有弹幕存入danmu_detail
section_cid = get_cid(index_url)
[get_danmu(each_section['cid']) for each_section in section_cid]

filename = 'danmu.txt'
with open(filename,'w',encoding='utf-8') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    for i in danmu_detail:
        f.write(str(i['danmu'])+'\n')