# coding: utf-8
import subprocess

start_server = "python 1.servers.py"
start_url_2_m3u8 = "python 2.url_2_m3u8.py"
start_m3u8_down = "python 3.m3u8_down.py"
start_webio = "python 4.webio.py"
start_reids = ".\\redis-server.exe redis.windows.conf"


if __name__ == '__main__':
    print("start redis")
    subprocess.Popen(start_reids, shell=True)
    print("start server")
    subprocess.Popen(start_server, shell=True)
    print("start url_2_m3u8")
    subprocess.Popen(start_url_2_m3u8, shell=True)
    print("start m3u8_down")
    subprocess.Popen(start_m3u8_down, shell=True)
    print("start webio")
    subprocess.run(start_webio, shell=True)
