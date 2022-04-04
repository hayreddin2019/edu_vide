# coding: utf-8
import redis
import os
from urllib.parse import quote


r = redis.Redis(host='localhost', port=6379, db=1)

while True:
    get_data = r.blpop('m3u8_down_link')[1].decode('utf-8')
    url_name = get_data.split('$')[0]
    url_link = get_data.split('$')[1]
    url = url_link.split('|')[0]
    work_dir = url_link.split('|')[1].split('@')[1]
    print("获取到m3u8地址: ", url)
    url = quote(url, safe="/:?=&%20")
    print("转码后的m3u8地址: ", url)
    print("正在下载 m3u8 文件", url)
    os.system("edu_video.exe" + " " + url + " " + "--headers" + " " + "referer:https://www.zxx.edu.cn/" + " " + "--workDir" + " " + work_dir + " " + "--saveName" + " " + url_name)
    print("该文件下载完成！")
