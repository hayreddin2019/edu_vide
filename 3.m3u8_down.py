# coding: utf-8
import redis
import os
import psutil

r = redis.Redis(host='localhost', port=6379)

while True:
    url = r.blpop('m3u8_url')[1].decode('utf-8')
    print("获取到m3u8地址: ", url)
    pl = psutil.pids()
    print("正在下载 m3u8 文件", url)
    os.system("edu_video.exe" + " " + url)
    print("该文件下载完成！")

