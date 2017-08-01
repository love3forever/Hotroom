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
