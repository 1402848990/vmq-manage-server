47.243.215.58
n5TjyGab7Xyrw4fPx0n7
ubuntu22.04

<!-- 云机 -->
18184693790
Asdasd11.



19317342383    
Qwe123123++


<!-- 打包 -->
pyinstaller --onefile --windowed --hidden-import=comtypes --hidden-import=comtypes.stream --add-data "logo.ico;." --icon=logo.ico  --name=账号管理系统 vmq管理.py


<!-- 查看日志 -->
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log

<!-- 结束进程 -->
# 结束所有 Gunicorn 进程（按命令名匹配）
pkill gunicorn


<!-- 重启流程 -->
<!-- 先结束进程 -->
pkill -f gunicorn 

<!-- 判断是否结束 -->
ps aux | grep gunicorn

cd /var/vmq

nohup gunicorn \
  --bind 0.0.0.0:5500 \
  --workers 2 \
  --timeout 60 \
  --access-logfile /var/log/gunicorn/access.log \
  --error-logfile /var/log/gunicorn/error.log \
  --log-level info \
  app:app > /var/log/gunicorn/gunicorn.out 2>&1 &


  <!-- 查看进程 -->
  ps aux | grep gunicorn