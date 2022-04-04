# coding: utf-8

import redis
import requests

r = redis.Redis(host='localhost', port=6379, db=1)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"}


def get_book_info(book_id):
    active_url = f"https://s-file.ykt.cbern.com.cn/x_course_s_g/s_course/v2/business_courses/{book_id}/course_relative_infos/zh-CN.json"
    book_active = requests.get(active_url, headers=header).json()
    print("获取到数据为:", book_active)
    try:
        book_active_code = book_active['course_detail']['activity_set_id']
        book_name = book_active['course_detail']['name']
    except KeyError:
        return False, None
    print("推送完成")
    print(f"成功从{book_id}推送课本UID:{book_active_code}")
    return book_active_code, book_name

