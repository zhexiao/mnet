var server_host = "http://192.168.33.20:8000"
var _ip = location.href.replace(/.*ip=/, '')

$(function(){
    $('.ip-name').html(_ip)
    generate_netflow_src_ip_stats()
    generate_chart_1()
})

/**
 * 生成netflow SRC IP stats
 */
function generate_netflow_src_ip_stats(){

    var _chart = echarts.init($('.netflow-src-ip-stats')[0]);

    $.ajax({
        url: server_host+'/netflow/netflow_ip_stats?type=src&ip='+_ip,
        type: 'get',
        dataType: 'json'
    }).done(function(res){
        var _series_data = [], _legend_data = [];
        for (_ip in res) {
            _legend_data.push(_ip)
            _series_data.push({
                'name': _ip,
                'value': res[_ip]
            })
        }

        var option = {
            title: {
                text: '源IP - 与其交流的目的IP占比'
            },
            tooltip: {
                trigger: 'item',
            },
            legend: {
                orient: 'vertical',
                left: 'right',
                data: _legend_data
            },
            series: [
                {
                    name: '目的IP',
                    type: 'pie',
                    radius: '55%',
                    center: ['50%', '60%'],
                    data: _series_data,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
    })
}

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
        var legend_list = [], bytes_list = [],
            flows_list = [], packets_list = [];

        for (key in res){
            legend_list.push(res[key]['datetime'])
            bytes_list.push(res[key]['bytes'])
            flows_list.push(res[key]['flows'])
            packets_list.push(res[key]['packets'])
        }

        var option = {
            title: {
                text: '源IP时间段 - 数据平均值'
            },
            tooltip: {
                trigger: 'axis',
            },
            legend: {
                data: ['flows(K)', 'packets(K)', 'bytes(MB)']
            },
            xAxis: [
                {
                    type: 'category',
                    data: legend_list
                }
            ],
            yAxis: [
                {
                    type: 'value',
                }
            ],
            series : [
                {
                    name: 'flows(K)',
                    type: 'line',
                    data: flows_list,
                },
                {
                    name: 'bytes(MB)',
                    type: 'line',
                    data: bytes_list,
                },
                 {
                    name: 'packets(K)',
                    type: 'line',
                    data: packets_list,
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        chart_1.setOption(option);
    })
}
