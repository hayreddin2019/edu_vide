# coding: utf-8

import redis

r = redis.Redis(host='localhost', port=6379)

while True:
    m3u8_sig = r.blpop('queue')
    sig_list = m3u8_sig[1].decode(encoding='utf-8', errors='strict').split(',')
    for i in sig_list:
        r.lpush('html_url', i)
        print("成功推送UID", i)
    print("推送完成")
