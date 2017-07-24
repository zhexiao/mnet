# mnet

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
