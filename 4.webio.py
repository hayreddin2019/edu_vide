# coding: utf-8
import pywebio
from pywebio import input, output
from pywebio import config
import json
import redis
import os

r = redis.Redis(host='localhost', port=6379)


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
            for i in _json_file:
                jie_duan = i["nianJiList"]
                for j in jie_duan:
                    _grade_list.append([j["njName"], num])
                num += 1
            return _grade_list

        def get_xue_ke_id(jie_duan, grade_num):
            subject_list = []
            num = 0
            for i in json_file:
                if num != jie_duan:
                    num += 1
                    continue
                xue_ke = i["nianJiList"][grade_num]
                for i in xue_ke["subjectsList"]:
                    subject_list.append(i["xkName"])
                num += 1
            return subject_list

        def get_all_vid(jie_duan, grade, subject):
            all_vid = []
            json_content = json_file[jie_duan]["nianJiList"][grade]["subjectsList"][subject]
            for i in json_content["danYuanList"]:
                for j in i["caseList"]:
                    all_vid.append(j["caseCode"])
            return all_vid

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

        work_dir = input.input("请输入要保存的目录[相对路径]（会覆盖还没有运行的任务!）：", value="/Downloads")
        r.set("work_dir", work_dir)
        work_dir = os.getcwd() + r.get('work_dir').decode('utf-8').replace('/', '\\')
        output.toast(f"添加工作目录为{work_dir}", color="success")
        gread_str = input.select("请选择年级", grade_temp_list)
        jieduan_num = int(gread_str.split('-')[0])
        grade_num = int(gread_str.split('-')[1]) - 1

        xue_ke = get_xue_ke_id(jieduan_num, grade_num)

        xue_ke_str = input.select("请选择学科", xue_ke)

        for i in xue_ke:
            if xue_ke_str == i:
                xue_ke_num = xue_ke.index(i)

        all_vid = get_all_vid(jieduan_num, grade_num, xue_ke_num)

        for i in all_vid:
            r.lpush("queue", i)
            output.put_markdown(f"已经推送{i}至下载队列，请稍后查看或者刷新页面重新添加")
        print("推送完成")
        output.toast("添加完成，请注意不要重复添加，否则会导致重复下载", color="error")
        # 选择要下载的年级


if __name__ == '__main__':
    pywebio.platform.tornado_http.start_server(main, port=3985, host='', debug=False, cdn=True, static_dir=None,
                                               allowed_origins=None, check_origin=None, auto_open_webbrowser=False,
                                               session_expire_seconds=None, session_cleanup_interval=None,
                                               max_payload_size='200M')
    # start_server(main, debug=True, port=3985, cdn="https://s-bj-2220-tuo-admin.oss.dogecdn.com/")
