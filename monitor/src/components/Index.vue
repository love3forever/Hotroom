<template>
  <div class="jumbotron">  
    <router-link to="/douyu/index">
      <img src="static/douyu_logo.png" class="img-thumbnail">
    </router-link>
    <router-link to="/panda/index">
      <img src="static/panda_logo.jpeg" class="img-thumbnail">      
    </router-link>
    <router-link to="/quanmin/index">
      <img src="static/quanmin_logo.jpg" class="img-thumbnail">      
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

img {
  height: 200px;
  width: 200px;
}
</style>
