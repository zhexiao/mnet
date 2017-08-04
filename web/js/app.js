var server_host = "http://192.168.33.20:8000"

$(function(){
    generate_top_flow()
    generate_chart_2()
    generate_chart_3()
})

function generate_top_flow(){
    var _chart = echarts.init($('.chart-1-body')[0]);

    $.ajax({
        url: server_host+'/netflow/ip_date_records?type=src',
        type: 'get',
        dataType: 'json'
    }).done(function(res){
        var series_data = [], ip_list = [], datetime_list = [];

        for (ip in res){
            var tmp = {
                'name': ip,
                'type': 'line',
                'data': []
            }
            ip_list.push(ip)
            for (key in res[ip]) {
                tmp['data'].push(res[ip][key]['avg_flow'])
            }

            series_data.push(tmp)
        }

        for (key in res[ip_list[0]]){
            datetime_list.push(res[ip_list[0]][key]['datetime'])
        }

        var option = {
            title: {
                text: 'Top7源IP - flow平均值'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ip_list
            },
            xAxis: [
                {
                    type: 'category',
                    data: datetime_list
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'flows'
                }
            ],
            series : series_data
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
        var flows_list = [], packets_list = [], bytes_list = [], ip_lists = [];
        for (key in res){
            ip_lists.push(res[key]['ip'])
            flows_list.push(res[key]['flows'])
            packets_list.push(res[key]['packets'])
            bytes_list.push(res[key]['bytes'])
        }

        var option = {
            title: {
                text: '源IP - 平均值'
            },
            tooltip: {
                trigger: 'axis',
               axisPointer: {
                   type: 'shadow'
               }
            },
            legend: {
                data: ['bytes(MB)', 'flows(K)', 'packets(K)']
            },
            xAxis: {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: ip_lists
            },
            series : [
                {
                    name: 'bytes(MB)',
                    type: 'bar',
                    stack: '总量',
                    data: bytes_list
                },
                {
                    name: 'flows(K)',
                    type: 'bar',
                    stack: '总量',
                    data: flows_list
                },
                {
                    name: 'packets(K)',
                    type: 'bar',
                    stack: '总量',
                    data: packets_list
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        _chart.setOption(option);
        _chart.on('click', function (params) {
            window.location.href="/app/ip_details.html?ip="+encodeURIComponent(params.name)
        });
    })
}
