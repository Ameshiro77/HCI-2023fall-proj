export default function buildPredictConfig (xAxis,predictNum, predictConfirm) {
    return {
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
          data: predictNum
        },
        {
          name: '累计感染(包括无症状)',  //换为治愈
          type: 'line',
          smooth: true,
          data: predictConfirm
        },
      ]
    }
  }
  