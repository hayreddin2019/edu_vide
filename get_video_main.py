# coding:utf-8

import re
import requests


def get_content(_url):
    try:
        response = requests.get(_url, timeout=10)
        if response.status_code == 200:
            print("获取页面成功")
            return response.content.decode('utf-8')
        else:
            return None
    except requests.RequestException:
        return None


def content_re_m3u8(_content):
    m3u8_content = re.findall('file: "(.*?)",', _content)[0]
    return m3u8_content


def url_to_m3u8(_url):
    _url = "https://tongbu.eduyun.cn/tbkt/tbkthtml/wk/weike/" + _url[:6] + "/" + _url + ".html"
    content = get_content(_url)
    m3u8_content = content_re_m3u8(content)
    return m3u8_content

