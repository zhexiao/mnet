#!/bin/bash
########################
# 服务器执行脚本
#######################
type=$1
app=$2

cmd=""
runserver="python manage.py runserver 0.0.0.0:8080"
migration_all="python manage.py makemigrations"
migrate_all="python manage.py migrate"

function run_cmd(){
	echo $cmd
	eval $cmd
}

if [ $type = "server" ]
then
	cmd=$runserver
elif [ $type = "migration_all" ]
then
	cmd=$migration_all
elif [ $type = "migration" ]
then
	cmd=$migration_all" $app"
elif [ $type = "migrate_all" ]
then
	cmd=$migrate_all
elif [ $type = "migrate" ]
then
	cmd=$migrate_all" $app"
fi

# 运行
run_cmd
