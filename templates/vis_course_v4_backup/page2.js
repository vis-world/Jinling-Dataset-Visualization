
// 步骤3：初始化echarts实例对象
var charts = [];
for (let i = 1; i <= 1; i++) {
    var chart = echarts.init(document.querySelector('#radar' + i));
    charts.push(chart);
}


//雷达图
var radarOption = {
    // title: {
    //     text: 'Basic Radar Chart'
    // },
    legend: {
        data: ['Allocated Budget', 'Actual Spending']
    },
    radar: {
        // shape: 'circle',
        "radius": '60%',
        indicator: [
            { name: 'Sales', max: 6500 },
            { name: 'Administration', max: 16000 },
            { name: 'Information Technology', max: 30000 },
            { name: 'Customer Support', max: 38000 },
            { name: 'Development', max: 52000 },
            { name: 'Marketing', max: 25000 }
        ]
    },
    series: [
        {
            name: 'Budget vs spending',
            type: 'radar',
            data: [
                {
                    value: [4200, 3000, 20000, 35000, 50000, 18000],
                    name: 'Allocated Budget'
                },
                {
                    value: [5000, 14000, 28000, 26000, 42000, 21000],
                    name: 'Actual Spending'
                }
            ]
        }
    ]
};

var radarOption1 = {
    // title: {
    //     text: 'Basic Radar Chart'
    // },
    legend: {
        data: ['数值1', '数值2']
    },
    radar: {
        "radius": '60%',
        // shape: 'circle',
        indicator: [
            { name: 'A', max: 100 },
            { name: 'B', max: 100 },
            { name: 'C', max: 100 },
            { name: 'D', max: 100 },
            { name: 'E', max: 100 },
            { name: 'F', max: 100 },
            { name: 'G', max: 100 },
        ]
    },
    series: [
        {
            name: 'Budget vs spending',
            type: 'radar',
            data: [
                {
                    value: [82, 90, 80, 75, 70, 98, 100],
                    name: '数值1'
                },
                {
                    value: [50, 14, 28, 26, 42, 21, 100],
                    name: '数值2'
                }
            ]
        }
    ]
};

var radarOption_All = {
    "legend": {
        "data": [
            "李白", "袁枚", "刘禹锡", "郭茂倩", "朱元璋", "王安石"
        ]
    },
    "radar": {
        "radius": '60%',
        "indicator": [
            { "name": "综合评价", "max": 100, color: '#ff0000' },
            { "name": "作品数", "max": 100 },
            { "name": "相关作品数", "max": 100 },
            { "name": "相关人物数", "max": 100 },
            { "name": "地点数", "max": 100 },
            { "name": "文体数", "max": 100 }
        ]
    },
    "series": [
        {
            "name": "诗人评分",
            "type": "radar",
            "data": [
                {
                    "value": [100, 100, 20, 50, 100, 70],
                    "name": "李白"
                },
                {
                    "value": [78, 65, 45, 14, 21, 100],
                    "name": "袁枚"
                },
                {
                    "value": [77, 17, 100, 85, 15, 23],
                    "name": "刘禹锡"
                },
                {
                    "value": [72, 1, 100, 100, 0, 5],
                    "name": "郭茂倩"
                },
                {
                    "value": [67, 38, 0, 92, 8, 52],
                    "name": "朱元璋"
                },
                {
                    "value": [55, 63, 20, 7, 23, 47],
                    "name": "王安石"
                }
            ]
        }
    ]
}

var radarOption_Top1 = {
    "tooltip": {
        "trigger": 'item',
        "formatter": function (params) {
            let result = params.seriesName + ' - ' + params.name + '<br/>';
            params.value.forEach(function (value, i) {
                result += radarOption_Top1.radar.indicator[i].name + ' : ' + value + '<br/>';
            });
            return result;
        }
    },
    "legend": {
        // "left": '10%',
        "data": [
            "李白", "平均值"
        ],
        "itemGap": 70
    },
    "radar": {
        "radius": '60%',
        "indicator": [
            { "name": "综合评价", "max": 150, color: '#cf395d' },
            { "name": "作品数", "max": 150, color: '#cf395d' },
            { "name": "相关作品数", "max": 150, color: '#cf395d' },
            { "name": "相关人物数", "max": 150, color: '#cf395d' },
            { "name": "地点数", "max": 150, color: '#cf395d' },
            { "name": "文体数", "max": 150, color: '#cf395d' }
        ]
    },
    "series": [
        {
            "name": "诗人评分",
            "type": "radar",
            "data": [
                {
                    "value": [150, 150, 70, 100, 150, 120],
                    "name": "李白",
                    lineStyle: {
                        normal: {
                            color: '#1781b5' // 李白数据系列的线条颜色
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: '#c3d7df',
                            opacity: 0.5 // 李白数据系列的区域填充透明度
                        }
                    }
                },
                {
                    "value": [
                        60.85,  // 综合评价 average_grade
                        58.47,   // 作品数 average_work
                        65.98,  // 相关作品数 average_rwork
                        63.24,  // 相关人物数 average_rauthor
                        56.21,   // 地点数 average_place
                        62.74   // 文体数 average_type
                    ],
                    "name": "平均值",
                    lineStyle: {
                        normal: {
                            color: '#dc9123' // 平均值数据系列的线条颜色
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: '#fbb957', // 平均值数据系列的线条颜色
                            opacity: 0.2 // 平均值数据系列的区域填充透明度
                        }
                    },
                    itemStyle: {
                        color: '#e7a23f' // 节点颜色
                    }
                }
            ]
        }
    ]
};

charts.forEach(chart => {
    chart.setOption(radarOption);
});
charts[0].setOption(radarOption_Top1);
/* charts[1].setOption(radarOption_Top2);
charts[2].setOption(radarOption_Top3);
charts[3].setOption(radarOption_Top4);
 */

window.addEventListener('resize', function () {
    charts.forEach(chart => {
        chart.resize();
    });
});
