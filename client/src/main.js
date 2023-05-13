import { createApp } from 'vue'
import * as echarts from "echarts"
import App from './App.vue'

Vue.prototype.$echarts = echarts;
createApp(App).mount('#app')
