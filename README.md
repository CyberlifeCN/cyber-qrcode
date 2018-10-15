# cyber-qrcode
cyber-qrcode by tornado.
make rpm package on centos7, but I think this project can run on anything linux.

## 功能
* 由输入的URL生成二维码
* 生成图片校验码


## 安装软件包
### 安装 nginx
```
yum -y install nginx
systemctl start nginx
systemctl enable nginx
```
### 安装 pip
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
### 安装 tornado
```
pip install --upgrade pip
pip install tornado==4.3
```
### 安装python依赖包
```
yum install git
git clone https://github.com/SerenaFeng/tornado-swagger.git
cd tornado-swagger
python setup.py install
```
### 安装qrcode
```
pip install qrcode
```
### 安装PIL
```
yum install python-imaging
```

## 安装 cyber-qrcode
```
rpm -Uvh cyber-qrcode-1.0.0-3_git_ed98137.x86_64.rpm --force
```

## API文档
http://qrcode.cyber-life.cn/swagger/spec.html
