<template>
	<div class="index-wrap">
		<md-card>
			<md-card-content>
				<div class="chart-wrap" ref="chart1"></div>
			</md-card-content>
		</md-card>

		<md-card>
			<md-card-content>
				<div class="chart-wrap" ref="chart2"></div>
			</md-card-content>
		</md-card>
	</div>
</template>

<script>
	export default {
		name: 'index',
		data(){
			return {
				seen: true
			}
		},
		mounted(){
			this.init_chart1()
			this.init_chart2()
		},
		methods: {
			init_chart1() {
				var _chart = this.$echarts.init(this.$refs['chart1']);

				this.$ajax({
					method: 'get',
					url: consts.api_server + '/stats_ip/date_history?type=src',
					dataType: 'json'
				}).then(function(res){
					var series_data = [], ip_list = [], datetime_list = [];
					var data = res['data']
					for (var ip in data){
						var tmp = {
							'name': ip,
							'type': 'line',
							'data': []
						}
						ip_list.push(ip)
						for (var key in data[ip]) {
							tmp['data'].push(data[ip][key]['avg_flow'])
						}

						series_data.push(tmp)
					}

					for (var key in data[ip_list[0]]){
						datetime_list.push(data[ip_list[0]][key]['datetime'])
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
				})
			},
			init_chart2() {
				var _chart = this.$echarts.init(this.$refs['chart2']);
				this.$ajax({
					method: 'get',
					url: consts.api_server + '/stats_ip/total?type=src',
					dataType: 'json'
				}).then(function(res){
					var flows_list = [], packets_list = [], bytes_list = [], ip_lists = [];
					var data = res['data']

					for (var key in data){
						ip_lists.push(data[key]['ip'])
						flows_list.push(data[key]['flows'])
						packets_list.push(data[key]['packets'])
						bytes_list.push(data[key]['bytes'])
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
				})
			}
		}
	}
</script>
