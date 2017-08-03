var server_host = "http://192.168.33.20:8000"
var _ip = location.href.replace(/.*ip=/, '')

$(function(){
    $('.ip-name').html(_ip)
    generate_chart_1()
    generate_chart_2()
})

/**
 * 生成图表1
 */
function generate_chart_1(){
    var chart_1 = echarts.init($('.chart-1-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_date_records?type=src&ip='+_ip,
        type: 'get',
        dataType: 'json'
    }).done(function(res){

        var option = {
            title: {
                text: '作为源IP-时间段数据平均值'
            },
            tooltip: {
                trigger: 'axis',
            },
            legend: {
                data: ['flows', 'bytes(MB)', 'packets(K)']
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
                }
            ],
            series : [
                {
                    name: 'flows',
                    type: 'line',
                    data: res['flows'],
                },
                {
                    name: 'bytes(MB)',
                    type: 'line',
                    data: res['bytes'],
                },
                 {
                    name: 'packets(K)',
                    type: 'line',
                    data: res['packets'],
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        chart_1.setOption(option);
    })
}

/**
 * 生成图表2
 */
function generate_chart_2(){
    var _chart = echarts.init($('.chart-2-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_date_records?type=dst&ip='+_ip,
        type: 'get',
        dataType: 'json'
    }).done(function(res){

        var option = {
            title: {
                text: '作为目的IP-时间段数据平均值'
            },
            tooltip: {
                trigger: 'axis',
            },
            legend: {
                data: ['flows', 'bytes(MB)', 'packets(K)']
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
                }
            ],
            series : [
                {
                    name: 'flows',
                    type: 'line',
                    data: res['flows'],
                },
                {
                    name: 'bytes(MB)',
                    type: 'line',
                    data: res['bytes'],
                },
                 {
                    name: 'packets(K)',
                    type: 'line',
                    data: res['packets'],
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
    })
}
