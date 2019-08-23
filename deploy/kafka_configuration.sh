#!/bin/bash -e

function update_config() {
    # 更新配置文件的函数
    config_name=$1
    config_val=$2
    filename=$3

    echo "[Configuring] $env_name in $filename"
    
    # 如果配置名在文件里面找到了
    if grep -E -q "^#?$config_name=.*" "$filename"
    then
    	echo "update $config_name | $config_val | $filename"
    	# 直接替换配置的值(因为替换的字符串可能包含有分隔符/，所以我们把分隔符s/a/b/g换成s@a@b@g)
    	sed -r -i "s@^#?$config_name=.*@$config_name=$config_val@g" "$filename"
    # 如果配置里面不存在配置
    else
    	# 追加到文件尾部
    	echo "append $config_name | $config_val | $filename"
        echo "$config_name=$config_val" >> "$filename"
    fi
}

# 不允许出现的配置参数
NOT_ALLOWED_ENV="|KAFKA_VERSION|KAFKA_HOME|KAFKA_DEBUG|KAFKA_GC_LOG_OPTS|KAFKA_HEAP_OPTS|KAFKA_JMX_OPTS|KAFKA_JVM_PERFORMANCE_OPTS|KAFKA_LOG|KAFKA_OPTS|"

# 循环系统环境变量
for env_var in $(env)
do

env_name=$(echo "$env_var" | cut -d "=" -f 1)

# 使用双括号可以用正则匹配符
if [[ $NOT_ALLOWED_ENV = *"|$env_name|"* ]]
then
    echo "[Invalid Env] $env_name"
    continue
fi

# 如果是以KAFKA为头的变量名
if [[ $env_name =~ ^KAFKA_ ]]
then
    # 把KAFKA_BROKER_ID=10转换成broker.id=10  
    # 按_分割取后面的所有值，把所有的大写转成小写，把所有的_转换成.
    env_full=$(echo "$env_var" |  cut -d _ -f 2- | tr '[:upper:]' '[:lower:]' | tr _ .)

    # 读取变量名和变量值
    config_name=$(echo "$env_full" | cut -d "=" -f 1)
    config_val=$(echo "$env_full" | cut -d "=" -f 2)

    # 更新变量文件
    update_config "$config_name" "$config_val" "$KAFKA_HOME/config/server.properties"
fi

done
