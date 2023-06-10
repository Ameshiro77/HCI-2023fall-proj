<template>
  <div>
    <!-- Header：标题和截止时间 -->
    <div class="data-statement">
      <div class="statement-title">{{ showname }}疫情状况</div>
      <div class="update-time">截止 {{ updateTime }}</div>
      <div class="shuoming" @click="handleModal"><span>数据说明</span></div>
    </div>

    <!-- 总的疫情数据统计 -->
    <e-summary :total="total" :today="today"></e-summary>

    <div class="all">

      <figure class="left-pic">
        <e-charts
          ref="line"
          :options="chinaDayList"
          :init-options="initOptions"
          autoresize
        ></e-charts>
      </figure>

      <div style="margin-top:5%;margin-left:1%">
        <el-button size="mini" type="primary" icon="el-icon-back" class="go" @click="goback"
          >返回
        </el-button>
      </div>

      <figure>
        <e-charts
          ref="map"
          :options="map"
          :init-options="initOptions"
          @click="handleClick"
          autoresize
        ></e-charts>
      </figure>


      <figure class="right-pic">
        <e-charts
          ref="line"
          :options="predictList"
          :init-options="initOptions"
          autoresize
        ></e-charts>
      </figure>
    </div>
    <div>
      <advice></advice>
    </div>
    <div class="section-title">国内病例</div>
    <e-table :data="table"></e-table>
  </div>
</template>

<script>
import buildMapData from "../data/map";
import EAlert from "../components/Alert";
import ETable from "../components/Table.vue";
import ECharts from "../components/ECharts.vue";
import ESummary from "../components/Summary.vue";
import { getNameByPinyin, getPinyinByName } from "../data/zhen";
import buildPredictConfig from "../data/config_predict";
import advice from "../components/advice.vue";
const axios = require("axios");
export default {
  components: {
    ETable,
    ECharts,
    ESummary,
    advice,
  },
  data() {
    return {
      updateTime: "",
      today: {},
      total: {},
      map: {},
      table: [],
      chinaDayList: null,
      provinceName: "",
      initOptions: {
        renderer: "canvas",
      },
      predictList: null, //用于存储预测的折线图数据
      showname: "", //显示省份名还是全国名
    };
  },
  methods: {
    handleClick(params) {
      this.update(params.name);
      this.getPredict(params.name);
      //this.$router.push(`/${provincePinyin}`)
    },
    //处理返回事件
    goback() {
      this.update(null); //传入null表示返回中国地图
    },
    //从后端获取预测数据并展示,传入省份名称
    getPredict(province) {
      let name = getPinyinByName(province);
      var req = axios.create({
        baseURL: `http://127.0.0.1:8081/predict?province_name=${name}`,
      });
      req.get("").then((res) => {
        let confirm = []; //累计确诊
        let num = []; //累计感染总数
        let xAxis = []; //x轴
        for (let i = 0; i < res.data[0].length; i++) {
          xAxis.push(i + 1); //先不标日期,从第1天开始
          confirm.push(res.data[0][i][0]);
          num.push(res.data[1][i][0]);
        }
        this.predictList = buildPredictConfig(xAxis, confirm, num);
      });
    },

    // 该函数为：点击数据说明，然后弹出画面
    handleModal() {
      EAlert({
        title: "数据说明",
        msg: `
          <div>
            <div>0. 数据爬取自【腾讯新闻】,在原有基础上增加了“省”一级的疫情地图。(仅供学习研究，<a href="https://github.com/border-1px/2019-nCov">[查看源代码]</a>)</div><br>
            <div>以下内容为腾讯数据声明：</div>
            <div>1. 全部数据来源于国家卫健委、各省卫健委以及权威媒体报道。</div><br>
            <div>2. 腾讯新闻的统计方法如下：</div>
            <div>
              a. 国家卫健委公布数据时，全国总数与国家卫健委保持一致。<br>
              b. 各省卫健委陆续公布数据，如果各省数据总和已经超过之前国家卫健委总数，则切换为直接使用各省数据总和。
            </div><br>
            <div>3. 国家卫健委及各省卫健委公布数据的发布时间和统计时间段各不相同，比如国家卫健委公布了最新全国数据，而各省还没有公布各自最新数据，故而会在部分时段出现国家总数不等于分省数据之和。</div>
          </div>
        `,
      });
    },
    async update(name) {
      console.log(name);
      const {
        updateTime,
        total,
        map,
        table,
        chinaDayList,
        today,
        province_name,
      } = await buildMapData(name);
      console.log(chinaDayList);
      this.chinaDayList = chinaDayList;
      this.updateTime = updateTime;
      this.today = today;
      this.total = total;
      this.table = table;
      this.map = map;
      this.showname = province_name;
    },
  },
  async created() {
    let province = this.$route.path.substr(1);
    this.provinceName = getNameByPinyin(province);
    console.log(this.provinceName);
    const { updateTime, total, map, table, chinaDayList, today } =
      await buildMapData(this.provinceName);

    this.chinaDayList = chinaDayList;
    console.log(this.chinaDayList);
    this.updateTime = updateTime;
    this.today = today;
    this.total = total;
    this.table = table;
    this.map = map;
    this.getPredict("上海");
  },
};
</script>
<style>
.left-pic {
  width: 30%;
  border: 1px solid #999;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  margin-left:1%;
}
.right-pic {
  width: 30%;
  border: 1px solid #999;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  /* margin-right:1%; */
}
.all {
  margin-top: 10px;
  display: flex;
  width: 100%;
}
.go {

}
</style>
