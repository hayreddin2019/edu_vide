# coding: utf-8

import redis
from get_video_main import url_to_m3u8

r = redis.Redis(host='localhost', port=6379)


while True:
    url = r.blpop("html_url")[1].decode('utf-8')
    print("正在尝试转换:", url)
    m3u8_str = url_to_m3u8(url)
    if m3u8_str:
        r.rpush("m3u8_url", m3u8_str)
        print("转换成功:", m3u8_str)
    else:
        print("转换失败，尝试重新转换:", url)
        r.rpush("html_url", url)
        continue
    print("等待下一个url")
