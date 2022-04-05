# coding:utf-8
import json


# 读取 xue_duan.json 文件，获取学段的 url
def read_xue_duan_url():
    with open('xue_duan.json', 'r', encoding='utf-8') as f:
        _xue_duan_json = json.load(f)
    return _xue_duan_json


def chose_xue_duan_name(_xue_duan_json):
    print('请选择学段：')
    for i in _xue_duan_json["xueDuan"]:
        for k in i["nianJiList"]:
            print(k["njName"])
            print(k["subjectsList"])


if __name__ == '__main__':
    xue_duan_json = read_xue_duan_url()
    chose_xue_duan_name(xue_duan_json)
