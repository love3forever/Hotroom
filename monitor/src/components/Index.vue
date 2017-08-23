<template>
  <el-tabs v-model="defaultActive">
    <el-tab-pane label="游戏趋势" name="first"><gameIndex></gameIndex></el-tab-pane>
    <el-tab-pane label="热门主播" name="second">热门主播</el-tab-pane>
  </el-tabs>
</template>

<script>
import gameIndex from '@/components/games/gameIndex'
export default {
  name: 'Index',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      defaultActive: "first"
    }
  },
  components:{
    gameIndex:gameIndex
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
