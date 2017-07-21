import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import DouyuIndex from '@/components/douyu/douyu-index'
import QuanminIndex from '@/components/quanmin/quanmin-index'
import PandaIndex from '@/components/panda/panda-index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
    	path:'/douyu/index',
    	name:'DouyuIndex',
    	component:DouyuIndex
    },
    {
    	path:'/panda/index',
    	name:'PandaIndex',
    	component:PandaIndex
    },
    {
    	path:'/quanmin/index',
    	name:'QuanminIndex',
    	component:QuanminIndex
    }
  ]
})
