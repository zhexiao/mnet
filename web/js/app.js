var server_host = "http://192.168.33.20:8000"

$(function(){
    generate_chart_1()
    generate_chart_2()
    generate_chart_3()
})

function generate_chart_1(){
    var _chart = echarts.init($('.chart-1-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_date_records?type=src',
        type: 'get',
        dataType: 'json'
    }).done(function(res){
        var _series = [];
        var ip_list = []

        for (_key in res){
            if (_key == 'datetime'){
                continue
            }

            ip_list.push(_key)
            _series.push({
                'name': _key,
                'type':'line',
                'stack': '总量',
                'data': res[_key]['avg_flow']
            })
        }

        var option = {
            title: {
                text: 'Src IP flow平均值'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ip_list
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: res['datetime']
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'flows'
                }
            ],
            series : _series
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
        _chart.on('click', function (params) {
            window.location.href="/app/ip_details.html?ip="+encodeURIComponent(params.seriesName)
        });
    })
}

function generate_chart_2(){
    var _chart = echarts.init($('.chart-2-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_stats?type=src',
        type: 'get',
        dataType: 'json'
    }).done(function(res){

        var option = {
            title: {
                text: 'Src IP 平均值'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['bytes(KB)', 'flows', 'packets']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: res['ip']
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'bytes, flows'
                },
                {
                    type: 'value',
                    name: 'packets'
                }
            ],
            series : [
                {
                    name: 'bytes(KB)',
                    type: 'bar',
                    data: res['bytes']
                },
                {
                    name: 'flows',
                    type: 'bar',
                    data: res['flows'],
                },
                {
                    name: 'packets',
                    type: 'bar',
                    data: res['packets'],
                    yAxisIndex: 1
                },
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
        _chart.on('click', function (params) {
            window.location.href="/app/ip_details.html?ip="+encodeURIComponent(params.name)
        });
    })
}

function generate_chart_3(){
    var _chart = echarts.init($('.chart-3-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_stats?type=dst',
        type: 'get',
        dataType: 'json'
    }).done(function(res){

        var option = {
            title: {
                text: 'Dst IP 平均值'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['bytes(KB)', 'flows', 'packets']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: res['ip']
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'bytes, flows'
                },
                {
                    type: 'value',
                    name: 'packets'
                }
            ],
            series : [
                {
                    name: 'bytes(KB)',
                    type: 'bar',
                    data: res['bytes']
                },
                {
                    name: 'flows',
                    type: 'bar',
                    data: res['flows'],
                },
                {
                    name: 'packets',
                    type: 'bar',
                    data: res['packets'],
                    yAxisIndex: 1
                },
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
        _chart.on('click', function (params) {
            window.location.href="/app/ip_details.html?ip="+encodeURIComponent(params.name)
        });
    })
}
