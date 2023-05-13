 <!-- 准备具有宽高的容器 -->
 <div style="width: 100%; height: 100%" ref="chart"></div>

 <script>
let Echarts = require('echarts/lib/echarts'); //基础实例 注意不要使用import
require('echarts/lib/chart/bar'); //按需引入 bar = 柱状图
export default {
    data() { return { chart: null } }, //图表实例
    mounted() {
        window.addEventListener('resize', () => {
            this.chart.resize();
        });
    },
    methods: {
        init() {
            //2.初始化
            this.chart = Echarts.init(this.$refs.chart);
            //3.配置数据
            let option = {
                xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] }, //X轴
                yAxis: { type: 'value' }, //Y轴
                series: [{ data: [120, 200, 150, 80, 70, 110, 130], type: 'bar' }] //配置项
            };
            // 4.传入数据
            this.chart.setOption(option);
        }
    }
};
</script>