# coding: utf-8
import time
import redis
import requests

r = redis.Redis(host='localhost', port=6379, db=1)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"}


while True:
    get_data = r.blpop("m3u8_dan_yuan_id")[1].decode('utf-8')
    dan_yuan_id = get_data.split("@")[0]
    work_dir = get_data.split("@")[1]
    print("正在尝试转换:", dan_yuan_id)
    work_url = f"https://s-file.ykt.cbern.com.cn/x_course_s_g/s_course/v1/x_class_hour_activity/{dan_yuan_id}/resources.json"
    time.sleep(2)
    res = requests.get(work_url, headers=header)
    data = res.json()
    print(data)
    url_father = data[0]['video_extend']
    urls = url_father['urls'][-1]['urls']
    video_name = url_father['title']
    higher_url_01 = urls[0]
    higher_url_02 = urls[1]
    full_url = video_name + "$" + higher_url_01 + "|" + higher_url_02
    print("转换成功:", dan_yuan_id)
    r.rpush("m3u8_down_link", full_url + "@" + work_dir)
    print("已添加到队列:", full_url + "@" + work_dir)
