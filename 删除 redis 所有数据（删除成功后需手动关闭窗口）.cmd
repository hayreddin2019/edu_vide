chcp 65001
echo "按任意键（确认删除）或（关闭此窗口取消删除）！"
pause
del .\dump.rdb
.\redis-server.exe
.\redis-cli.exe flushall
EXIT