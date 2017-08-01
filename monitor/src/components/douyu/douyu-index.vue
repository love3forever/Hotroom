<template>
  <div id="douyu-app" class="container-fluid">
    <router-view></router-view>
    <div class="row" id="douyu-row1">
      <div id="douyu-dashboard" class="col-md-6"></div>
      <div id="douyu-top5-game" class="col-md-6"></div>
    </div>
    <div class="row" id="douyu-row2">
      <div id="douyu-timeline" class="col-md-12"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DouyuIndex',
  data () {
    return {
    }
  },
  methods: {
    get_games_with_heat:function(){

    }
  },
  mounted:function initEchart(){
    var douyu_chart = echarts.init(document.getElementById('douyu-dashboard'));
    
    var timeData = [];

    var timeData = timeData.map(function (str) {
        return str.replace('2009/', '');
    });

    var option = {
        title: {
            text: '雨量流量关系图',
            subtext: '数据来自西安兰特水电测控技术有限公司',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            }
        },
        legend: {
            data:['流量','降雨量'],
            x: 'left'
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
        axisPointer: {
            link: {xAxisIndex: 'all'}
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 30,
                end: 70,
                xAxisIndex: [0, 1]
            },
            {
                type: 'inside',
                realtime: true,
                start: 30,
                end: 70,
                xAxisIndex: [0, 1]
            }
        ],
        grid: [{
            left: 50,
            right: 50,
            height: '35%'
        }, {
            left: 50,
            right: 50,
            top: '55%',
            height: '35%'
        }],
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                axisLine: {onZero: true},
                data: timeData
            },
            {
                gridIndex: 1,
                type : 'category',
                boundaryGap : false,
                axisLine: {onZero: true},
                data: timeData,
                position: 'top'
            }
        ],
        yAxis : [
            {
                name : '流量(m^3/s)',
                type : 'value',
                max : 500
            },
            {
                gridIndex: 1,
                name : '降雨量(mm)',
                type : 'value',
                inverse: true
            }
        ],
        series : [
            {
                name:'流量',
                type:'line',
                symbolSize: 8,
                hoverAnimation: false,
                data:[
                ]
            },
            {
                name:'降雨量',
                type:'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                symbolSize: 8,
                hoverAnimation: false,
                data: [
                ]
            }
        ]
    };

    douyu_chart.setOption(option);
  }
}
</script>

<style>
#douyu-app {
  height: 100%;
}

#douyu-dashboard {
  height: 100%;
}

#douyu-row1 {
  height: 50%;
}

#douyu-row2 {
  height: 50%;
}
</style>
