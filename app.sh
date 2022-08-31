kill -9 $(cat supervisord.pid) # 杀掉进程
supervisord -c manager.conf