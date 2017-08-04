var server_host = "http://192.168.33.20:8000"

$(function(){
    generate_chart_1()
    generate_chart_2()
    generate_chart_3()
	generate_chart_4()
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
                'data': res[_key]['avg_flow']
            })
        }
        console.log(ip_list)
        console.log(_series)
        var option = {
            title: {
                text: 'Src IP flow平均值'
            },
            tooltip: {
                trigger: 'axis'
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