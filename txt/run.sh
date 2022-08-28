kill -9 $(cat supervisord.pid)
supervisord -c manager.conf