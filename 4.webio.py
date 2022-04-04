# coding: utf-8
import pywebio
from pywebio import input, output
from pywebio import config
from new_book import get_book_info
import json
import redis
import os

r = redis.Redis(host='localhost', port=6379)
r2 = redis.Redis(host='localhost', port=6379, db=1)


def new_version(work_dir):
    output.put_markdown(r"""新版说明如下""" + '\n' + '\n')
    vid_code = input.input("请输入视频编号：")
    active_id, book_name = get_book_info(vid_code)
    if active_id:
        output.toast("获取成功！", color="success")
        active_id = active_id + "@" + vid_code
        r2.lpush("active_id", active_id)
        output.put_markdown(f"已经推送 `{book_name}` 至下载队列，请在命令行窗口下载队列中查看")
    else:
        output.toast("获取失败，请检查并重新输入。", color="danger")
        new_version(work_dir)


@config(theme="yeti")
def main():
    while True:

        # 读取json文件
        def get_json():
            with open('xue_duan.json', 'r', encoding="utf-8") as f:
                content = json.load(f)
                return content['xueDuan']

        json_file = get_json()

        def get_grade(_json_file):
            _grade_list = []
            num = 0
            for _i in _json_file:
                jie_duan = _i["nianJiList"]
                for j in jie_duan:
                    _grade_list.append([j["njName"], num])
                num += 1
            return _grade_list

        def get_xue_ke_id(jie_duan, _grade_num):
            subject_list = []
            num = 0
            for _i in json_file:
                if num != jie_duan:
                    num += 1
                    continue
                _xue_ke = _i["nianJiList"][_grade_num]
                for j in _xue_ke["subjectsList"]:
                    subject_list.append(j["xkName"])
                num += 1
            return subject_list

        def get_all_vid(jie_duan, grade, subject):
            _all_vid = []
            json_content = json_file[jie_duan]["nianJiList"][grade]["subjectsList"][subject]
            for _i in json_content["danYuanList"]:
                for j in _i["caseList"]:
                    _all_vid.append(j["caseCode"])
            return _all_vid

        grade_list = get_grade(json_file)
        # print(grade_list)
        # print(get_xue_ke_id(0, 11))
        # print(get_all_vid(0, 0, 0))

        # 公告部分
        output.put_markdown(r""" # 🚀 欢迎使用 `EDU` 视频下载工具
        ### 首先，你应该知道的是
        - 本工具仅供学习交流，不得用于商业用途
        - 使用本工具的风险由你自己承担
        - 本工具仅提供视频下载功能，不提供视频播放功能
        - OK，开始使用吧！
            """)

        grade_temp_list = []

        temp = 0
        temp2 = 0
        for i in grade_list:
            if temp == i[1]:
                temp2 += 1
            else:
                temp2 = 0
                temp += 1
            grade_temp_list.append(str(i[1]) + '-' + str(temp2) + '-' + i[0])
        down_dir_value = os.getcwd() + '\download'
        work_dir = input.input("请输入要保存的目录[绝对路径]（只对本次任务有效）：", value=down_dir_value)
        output.toast(f"添加工作目录为{work_dir}(只对本次任务有效)", color="success")
        version_list = ["旧版: https://ykt.eduyun.cn/ykt/index.html", "新版: https://www.zxx.edu.cn/syncClassroom"]
        version_chose = input.select("请选择版本：", version_list)
        if version_chose == "新版: https://www.zxx.edu.cn/syncClassroom":
            new_version(work_dir)
            continue
        else:
            pass
        grade_str = input.select("请选择年级", grade_temp_list)
        jie_duan_num = int(grade_str.split('-')[0])
        grade_num = int(grade_str.split('-')[1]) - 1

        xue_ke = get_xue_ke_id(jie_duan_num, grade_num)

        xue_ke_str = input.select("请选择学科", xue_ke)

        for i in xue_ke:
            if xue_ke_str == i:
                xue_ke_num = xue_ke.index(i)

        all_vid = get_all_vid(jie_duan_num, grade_num, xue_ke_num)

        for i in all_vid:
            i = i + "@" + work_dir
            r.lpush("queue", i)
            output.put_markdown(f"已经推送{i}至下载队列，请在命令行窗口下载队列中查看")
        print("推送完成")
        output.toast("添加完成，请注意不要重复添加，否则会导致重复下载", color="error")
        # 选择要下载的年级


if __name__ == '__main__':
    pywebio.platform.tornado_http.start_server(main, port=3985, host='', debug=False, cdn=True, static_dir=None,
                                               allowed_origins=None, check_origin=None, auto_open_webbrowser=False,
                                               max_payload_size='200M')
    # start_server(main, debug=True, port=3985, cdn="https://s-bj-2220-tuo-admin.oss.dogecdn.com/")
