<template>
  <div>
    <!-- Header：标题和截止时间 -->
    <div class="all">
      <div class="left_pic">
      <detect @left_event="updateleftLine" @right_event="updaterightLine" />
    </div>
    <div style="width: 70%;display: flex;justify-content: center;align-items: center;">
      <span class="title">疫情可视化系统</span>
    </div>
    </div>
    <div class="data-statement">
      <div class="statement-title">{{ showname }}疫情状况</div>
      <div class="update-time">截止 {{ updateTime }}</div>
      <div class="shuoming" @click="handleModal"><span>数据说明</span></div>
    </div>
    <!-- 总的疫情数据统计 -->
    <e-summary :total="total" :today="today"></e-summary>

    <div class="all">
      <!-- 左边图 -->
      <figure class="left-pic">
        <e-charts
          ref="left_line"
          :options="chinaDayList"
          :init-options="initOptions"
          autoresize
        ></e-charts>
      </figure>

      <!-- 中间地图 -->
      <div style="margin-top: 5%; margin-left: 1%">
        <el-button
          size="mini"
          type="primary"
          icon="el-icon-back"
          class="go"
          @click="goback"
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

      <!-- 右边地图 -->
      <figure class="right-pic">
        <e-charts
          ref="right_line"
          :options="predictList"
          :init-options="initOptions"
          autoresize
        ></e-charts>
      </figure>
    </div>

    <!-- 医疗建议 -->
    <div class="medical-advice">
      <el-card style="border-radius: 8px; width: 100%">
        <div style="text-align: left; line-height: 18px">
          <span> 当前 </span>
          <span style="font-weight: bold">{{ displayName }}地区</span>
          <span> 疫情程度：{{ classify }}</span>
        </div>
        <div style="text-align: left; line-height: 18px">
          <span> 医疗建议：{{ medical_advice }}</span>
        </div>
      </el-card>
    </div>

    <!-- 检测按钮 -->


    <!-- 国内病例 -->
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
import detect from "../components/detect.vue";
import echarts from "echarts";
const axios = require("axios");
const moment = require("moment");
export default {
  components: {
    ETable,
    ECharts,
    ESummary,
    advice,
    detect,
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
      displayName: "全国",
      initOptions: {
        renderer: "canvas",
      },
      predictList: null, //用于存储预测的折线图数据
      showname: "", //显示省份名还是全国名
      left_start: 0,
      left_end: 100,
      right_start: 0,
      right_end: 100,
      classify: "",
      medical_advice: "",
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
        const startDate = moment('2022-01-02', 'YYYY-MM-DD');

        const dateSeries = xAxis.map((index) => {
          return moment(startDate).add(index - 1, 'days').format('YYYY-MM-DD');
        });

        this.predictList = buildPredictConfig(dateSeries, confirm, num);
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

    // 更新数据
    async update(name) {
      console.log("name:", name);
      this.displayName = name;
      if (this.displayName == null) this.displayName = "全国";
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

      // 根据total获得建议和类别
      axios({
        method: "get",
        url: "http://127.0.0.1:8081/advice",
        params: {
          confirm: this.total.confirm,
          suspect: this.total.suspect,
          heal: this.total.heal,
          dead: this.total.dead,
        },
      })
        .then((response) => {
          console.log(response.data);
          this.classify = response.data.classify;
          this.medical_advice = response.data.advice;
        })
        .catch(() => {});
    },

    //进行左折线图更新
    updateleftLine(data) {
      let option = this.$refs.left_line.options;
      if (
        data.message == "small" &&
        option.dataZoom[0].end - option.dataZoom[0].start > 10
      ) {
        option.dataZoom[0].start += 1;
        option.dataZoom[0].end -= 1;
      } else if (
        data.message == "large" &&
        option.dataZoom[0].end - option.dataZoom[0].start < 100
      ) {
        option.dataZoom[0].start -= 1;
        option.dataZoom[0].end += 1;
      }

      this.$refs.left_line.option = option;
    },
    //子组件调用该方法进行右折线图缩放扩张
    updaterightLine(data) {
      let option = this.$refs.right_line.options;
      if (
        data.message == "small" &&
        option.dataZoom[0].end - option.dataZoom[0].start > 10
      ) {
        option.dataZoom[0].start += 1;
        option.dataZoom[0].end -= 1;
      } else if (
        data.message == "large" &&
        option.dataZoom[0].end - option.dataZoom[0].start < 100
      ) {
        option.dataZoom[0].start -= 1;
        option.dataZoom[0].end += 1;
      }

      this.$refs.right_line.option = option;
    },
  },

  async created() {
    let province = this.$route.path.substr(1);
    this.provinceName = getNameByPinyin(province);
    console.log("name:", this.provinceName);
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
  //子组件调用该方法进行左折线图缩放扩张
};
</script>
<style>
.left-pic {
  width: 30%;
  border: 1px solid #999;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  margin-left: 1%;
}
.right-pic {
  width: 30%;
  border: 1px solid #999;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  /* margin-right:1%; */
}

.medical-advice {
  padding: 10px;
  margin-top: 20px;
}

.all {
  margin-top: 10px;
  display: flex;
  width: 100%;
}
.go {
}
.title{
    font-size: 70px;
    font-weight: bold;
    color: rgb(66, 120, 133);
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);

}
</style>
