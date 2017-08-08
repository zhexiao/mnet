import Vue from 'vue'
import App from './App'
import router from './router'
Vue.config.productionTip = false

// 导入全局静态变量
import constants from '../config/constants';
global.consts = constants;

// material
import VueMaterial from 'vue-material'
Vue.use(VueMaterial)
// ajax
import axios from 'axios'
Vue.prototype.$ajax = axios
// echarts
import echarts from 'echarts'
Vue.prototype.$echarts = echarts

// css load
import 'vue-material/dist/vue-material.css'
import '../static/css/material-icon.css'
import '../static/css/app.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
