export default function buildLineConfig (xAxis, dataConfirm, dataSuspect, dataDead) {
  return {
    dataZoom: [{
      type: 'slider',  // 使用滑动条控制缩放
      xAxisIndex: 0,   // 设置控制的 x 轴索引
      start: 0,        // 默认缩放起始位置
      end: 100,        // 默认缩放结束位置
    }],
    title: {
      text: '疫情累计趋势(人)'
    },
    legend: {
      data: ['累计确诊', '累计治愈', '累计死亡'],
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
        data: dataConfirm
      },
      {
        name: '累计治愈',  //换为治愈
        type: 'line',
        smooth: true,
        data: dataSuspect
      },
      {
        name: '累计死亡',
        type: 'line',
        smooth: true,
        data: dataDead
      }
    ]
  }
}
