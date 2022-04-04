# coding: utf-8
import redis
import os
from urllib.parse import quote


r = redis.Redis(host='localhost', port=6379)

while True:
    get_data = r.blpop('m3u8_url')[1].decode('utf-8')
    url = get_data.split('@')[0]
    work_dir = get_data.split('@')[1]
    print("获取到m3u8地址: ", url)
    url = quote(url, safe="/:?=&%20")
    print("转码后的m3u8地址: ", url)
    print("正在下载 m3u8 文件", url)
    os.system("edu_video.exe" + " " + url + " " + "--headers" + " " + "referer:https://tongbu.eduyun.cn/" + " " + "--workDir" + " " + work_dir)
    print("该文件下载完成！")
