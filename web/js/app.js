$(function(){
    generate_top_flow()
    generate_chart_2()
	generate_chart_4()
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


function generate_chart_4() {
	var _chart = echarts.init($('.chart-4-body')[0]);
	var base = +new Date(2000, 9, 3);
	var oneDay = 24 * 3600 * 1000;
	var date = [];

	var data = [Math.random() * 300];

	for(var i = 1; i < 20000; i++) {
		var now = new Date(base += oneDay);
		date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
		data.push(Math.random() * 20 -10 + data[i - 1]);
	}

	option = {
		tooltip: {
			trigger: 'axis',
			position: function(pt) {
				return [pt[0], '10%'];
			}
		},
		title: {
			left: 'center',
			text: '大数据量面积图',
		},
		legend: {
			top: 'bottom',
			data: ['意向']
		},
		toolbox: {
			feature: {
				dataZoom: {
					yAxisIndex: 'none'
				},
				restore: {},
				saveAsImage: {}
			}
		},
		xAxis: {
			type: 'category',
			boundaryGap: false,
			data: date
		},
		yAxis: {
			type: 'value',
			boundaryGap: [0, '100%']
		},
		dataZoom: [{
			type: 'inside',
			start: 0,
			end: 10
		}, {
			start: 0,
			end: 10,
			handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
			handleSize: '80%',
			handleStyle: {
				color: '#fff',
				shadowBlur: 3,
				shadowColor: 'rgba(0, 0, 0, 0.6)',
				shadowOffsetX: 2,
				shadowOffsetY: 2
			}
		}],
		series: [{
			name: '数据',
			type: 'line',
			smooth: true,
			symbol: 'none',
			sampling: 'average',
			itemStyle: {
				normal: {
					color: 'rgb(255, 70, 131)'
				}
			},
			areaStyle: {
				normal: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
						offset: 0,
						color: 'rgb(255, 158, 68)'
					}, {
						offset: 1,
						color: 'rgb(255, 70, 131)'
					}])
				}
			},
			data: data
		}]
	};

	// 使用刚指定的配置项和数据显示图表。
	_chart.setOption(option);
}
