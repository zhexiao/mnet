$(function(){
    generate_chart_1()
    generate_chart_2()
})

/**
 * 生成图表1
 */
function generate_chart_1(){
    var chart_1 = echarts.init($('.chart-1-body')[0]);
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: 'chart 1'
        },
        tooltip: {},
        legend: {
            data:['bytes']
        },
        xAxis: {
            data: ["IP1","IP2","IP3","IP4","IP5","IP6"]
        },
        yAxis: {},
        series: [{
            name: 'bytes',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    chart_1.setOption(option);
}

/**
 * 生成图表2
 */
function generate_chart_2(){
    var chart_2 = echarts.init($('.chart-2-body')[0]);
    option = {
        title: {
            text: 'chart 2'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['IP1','IP2','IP3','IP4','IP5']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一','周二','周三','周四','周五','周六','周日']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'IP1',
                type:'line',
                stack: '总量',
                data:[120, 132, 101, 134, 90, 230, 210]
            },
            {
                name:'IP2',
                type:'line',
                stack: '总量',
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'IP3',
                type:'line',
                stack: '总量',
                data:[150, 232, 201, 154, 190, 330, 410]
            },
            {
                name:'IP4',
                type:'line',
                stack: '总量',
                data:[320, 332, 301, 334, 390, 330, 320]
            },
            {
                name:'IP5',
                type:'line',
                stack: '总量',
                data:[820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    chart_2.setOption(option);
}
