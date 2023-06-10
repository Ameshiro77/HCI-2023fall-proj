export default function buildPredictConfig (xAxis,predictNum, predictConfirm) {
    return {
      dataZoom: [{
        type: 'slider',  // 使用滑动条控制缩放
        xAxisIndex: 0,   // 设置控制的 x 轴索引
        start: 0,        // 默认缩放起始位置
        end: 100,        // 默认缩放结束位置

      }],
      title: {
        text: '疫情数据预测(人)'
      },
      legend: {
        data: ['累计确诊', '累计感染(包括无症状)'],
        top: '25',
        left: '0'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: true,
          data: xAxis
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: '累计确诊',
          type: 'line',
          smooth: true,
          data: predictNum,
          animation: true, // 启用过渡动画
          animationDuration: 1000, // 过渡动画持续时间，单位为毫秒
        },
        {
          name: '累计感染(包括无症状)',  //换为治愈
          type: 'line',
          smooth: true,
          data: predictConfirm,
          animation: true, // 启用过渡动画
          animationDuration: 1000, // 过渡动画持续时间，单位为毫秒
        },
      ]
    }
  }
  