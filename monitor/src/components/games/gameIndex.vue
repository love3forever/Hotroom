<template>
    <div id="game-index">
        <el-row :gutter="20">
          <el-col :span="24">
            <div class="grid-content bg-purple" id="game-heat-grid">
                <el-card class="box-card">
                  <div slot="header" class="clearfix">
                    <span style="line-height: 16px;">游戏热力</span>
                  </div>
                  <div id="game-heat">
                  </div>
                </el-card>
            </div>
          </el-col>
        </el-row>
        
    </div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'gameIndex',
  data () {
    return {
        heatChart:'',
        heatOption:{
            title: {
                text: '',
                textStyle:{
                    align:'center'
                }
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:[]
            },
            grid: {
                left: '5%',
                right: '5%',
                bottom: '4%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: []
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name:'',
                    type:'line',
                    stack: '总量',
                    data:[]
                }
            ]
        }
    };
  },
  methods: {
    initGameHeat:function(id){
        this.$http.get('http://127.0.0.1:5000/api/v1/douyu/game/%E7%BB%9D%E5%9C%B0%E6%B1%82%E7%94%9F/timeline').then(response => {
            let gameHeatData = response.body
            console.log(gameHeatData)
            this.heatOption.title.text = gameHeatData['catalog']
            this.heatOption.series[0].name = gameHeatData['catalog']
            for (var i = 0; i < gameHeatData['timeline'].length; i++) {
                let pairData = gameHeatData['timeline'][i]
                this.heatOption.series[0].data.push(pairData['count'])
                this.heatOption.xAxis.data.push(pairData['time'])
            }
            let worldMapContainer = document.getElementById(id)
            this.heatChart = echarts.init(document.getElementById(id))
            window.onresize = this.heatChart.resize
            this.heatChart.setOption(this.heatOption)
          }, response => {
            console.log('something wrong happened')
          });
        }
    },
  mounted: function(){
    this.initGameHeat('game-heat')        
    }

};
</script>

<style lang="css" scoped>
    .grid-content {
        border-radius: 4px;
        min-height: 500px;
    }
    .clearfix {
        text-align: left;
    }

    #game-heat {
        height: 450px;
        width: 100%;
    }
</style>