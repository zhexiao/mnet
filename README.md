# mnet

## 后端

#### 安装Mysql mysqlclient必备的依赖
```
> sudo apt-get install libmysqlclient-dev
```

#### 安装package
```
> pip install -r requirements.txt
```

#### pre-commit 安装
```
> pre-commit install
> pre-commit autoupdate
```

#### 运行服务器
```
> ./run.sh server
> ./run.sh migration_all
> ./run.sh migrate_all

# 单独app操作
> ./run.sh migration netflow
> ./run.sh migrate netflow
```

## 前端
安装SASS
```
1. install ruby:
    https://github.com/oneclick/rubyinstaller2/releases/download/2.4.1-2/rubyinstaller-2.4.1-2-x64.exe

2. open terminal and install sass:
    gem install sass
    sass -v
```

安装项目
```
1. clone 项目:
    git clone https://github.com/zhexiao/mnet.git

2. run sass:
    cd web
    sass --watch sass:css --no-cache --style compressed
```

编程工具和运行
```
1. 安装pycharm专业版
2. 右键web/app/index.html -> open in browser
```
