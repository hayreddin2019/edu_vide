# coding: utf-8
import redis
import requests

r = redis.Redis(host='localhost', port=6379, db=1)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"}


while True:
    get_data = r.blpop("active_id")[1].decode('utf-8')
    url_id = get_data.split("@")[0]
    work_dir = get_data.split("@")[1]
    print("正在尝试转换:", url_id)
    work_url = f"https://s-file.ykt.cbern.com.cn/x_course_s_g/s_course/v2/activity_sets/{url_id}/fulls.json"
    res = requests.get(work_url, headers=header)
    data = res.json()
    ke_cheng = data['nodes']
    for i in ke_cheng:
        print("正在转换:", i['node_name'])
        child_nodes = i['child_nodes']
        for j in child_nodes:
            print("成功推送:", j['node_name'], ":", j['node_id'])
            r.lpush("m3u8_dan_yuan_id", j['node_id'] + "@" + work_dir)
