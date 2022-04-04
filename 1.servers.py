# coding: utf-8

import redis

r = redis.Redis(host='localhost', port=6379)

while True:
    m3u8_sig = r.blpop('queue')
    sig_list = m3u8_sig[1].decode(encoding='utf-8', errors='strict')
    r.rpush('html_url', sig_list)
    print("成功推送UID", sig_list)
    print("推送完成")
