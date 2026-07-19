# Bass Studio 部署指南

## 服务器要求

- Ubuntu 24.04
- 2核 CPU / 2GB RAM（最低配置）
- Python 3.12+
- Nginx
- Git

## 部署步骤

### 1. 克隆项目

```bash
sudo mkdir -p /opt
cd /opt
sudo git clone https://github.com/your-username/BassStudio.git
sudo chown -R $USER:$USER /opt/BassStudio
```

### 2. 安装系统依赖

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip nginx
```

### 3. 配置后端

```bash
cd /opt/BassStudio/backend

# 创建虚拟环境
python3.12 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env  # 修改 SECRET_KEY 为随机字符串
```

### 4. 初始化数据库

```bash
cd /opt/BassStudio/backend
source venv/bin/activate
python init_data.py
```

⚠️ **重要：首次部署后立即修改管理员密码！** 默认账号: `admin` / `Admin@123456`

### 5. 构建前端

```bash
cd /opt/BassStudio/frontend

# 安装 Node.js (如未安装)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 安装依赖并构建
npm install
npm run build
```

### 6. 部署前端静态文件

```bash
sudo mkdir -p /var/www/bassstudio
sudo cp -r /opt/BassStudio/frontend/dist/* /var/www/bassstudio/
sudo chown -R www-data:www-data /var/www/bassstudio
```

### 7. 配置 Nginx

```bash
sudo cp /opt/BassStudio/deploy/nginx.conf.example /etc/nginx/sites-available/bassstudio
sudo nano /etc/nginx/sites-available/bassstudio  # 修改 server_name
sudo ln -s /etc/nginx/sites-available/bassstudio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

### 8. 配置 systemd 服务

```bash
sudo cp /opt/BassStudio/deploy/bassstudio.service.example /etc/systemd/system/bassstudio.service
sudo nano /etc/systemd/system/bassstudio.service  # 按需修改

sudo systemctl daemon-reload
sudo systemctl enable bassstudio
sudo systemctl start bassstudio

# 查看状态
sudo systemctl status bassstudio
```

### 9. 检查部署

```bash
# 检查后端
curl http://127.0.0.1:8000/api/health

# 检查前端
curl http://127.0.0.1/

# 查看日志
sudo journalctl -u bassstudio -f
sudo tail -f /var/log/nginx/bassstudio_access.log
```

## 更新部署

```bash
cd /opt/BassStudio
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart bassstudio

# 更新前端
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/bassstudio/
```

## 防火墙配置（可选）

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```
