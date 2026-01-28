47.243.215.58
n5TjyGab7Xyrw4fPx0n7
ubuntu22.04


8.210.94.60
7zd0e9209TncY92gLXdh

<!-- 北北服务器 -->
ubuntu
w1402848990W



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

  
<!-- 服务器部署流程 -->
<!-- 更新系统依赖 -->
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git

<!-- 上传代码 -->
sudo mkdir -p /var/www/account-api
sudo chown $USER:$USER /var/www/account-api

# 方法1：git clone（推荐）
cd /var/www/account-api
git clone https://your-repo/account-api.git .  # 替换为你的仓库

# 方法2：手动上传（如用 scp）
# scp -r ./local/project/* user@server:/var/www/account-api/

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask gunicorn pymysql sqlalchemy requests
# 如果用了其他库，也一并安装


<!-- 数据库 -->
# 安装 MySQL 服务器和客户端
sudo apt update
sudo apt install mysql-server mysql-client -y

<!-- 设置密码 -->
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
FLUSH PRIVILEGES;
EXIT;

<!-- 编辑配置文件 -->
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
<!-- 重启mysql -->
sudo systemctl restart mysql


-- 创建 root@% 用户（危险！）
mysql -u root -p
CREATE USER 'root'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

Sql
编辑
-- 登录 MySQL（sudo mysql）

FLUSH PRIVILEGES;
EXIT;

# 启动并设置开机自启
sudo systemctl start mysql
sudo systemctl enable mysql


<!-- 开启 -->
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 app:app