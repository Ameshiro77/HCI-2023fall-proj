import { createApp } from 'vue'
import * as echarts from "echarts"
import App from './App.vue'

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;

app.mount('#app');
