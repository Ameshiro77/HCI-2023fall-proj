import ECharts from '../components/ECharts.vue'
import { getPinyinByName } from '../data/zhen'
import buildLineConfig from './config_line'
import buildMapConfig from './config_map'
import chinaMap from '../data/china.json'
import area from './area.json'
const axios = require('axios')
function getProvince(province){
  return new Promise((resolve, reject) => {
    axios.get(`http://localhost:8080/provinces/${getPinyinByName(province)}.json`)
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        reject(error);
      });
  });
}
export default async function buildMapData (province) {
  var flag=1
  if(province==null){
    province='上海';
    flag=0;
  }
  const provinceData = await getProvince(province);
  console.log(provinceData)
  const mapData = {
    updateTime: area.lastUpdateTime,
    total: null,
    today: null,
    map: null,
    table: null,
    isProvince: false,
    chinaDayList: null
  }
  
  const provinces = area.areaTree[0].children
  var provincePinyin = getPinyinByName(province)
  const result = []
  const province_data=provinceData['historylist']
  //console.log(province_data)
  if (flag) {
    if(provincePinyin=='shanxis')provincePinyin='shanxi1';  //适应地图
    require(`echarts/map/js/province/${provincePinyin}`)
    // ECharts.registerMap(provincePinyin, provinceMap)

    const index = provinces.findIndex(p => {
      return p.name === province
    })

    mapData.isProvince = true
    mapData.total = provinces[index]['total']
    mapData.today = provinces[index]['today']
    mapData.table = provinces[index]['children']

    provinces[index]['children'].forEach(city => {
      result.push({
        name: city.cityName,
        value: city.total.confirm
      })
    })

    mapData.map = buildMapConfig(province, result)
  } else {
    ECharts.registerMap('china', chinaMap)

    provinces.forEach(p => {
      result.push({
        name: p.name,
        value: p.total.confirm
      })
    })
    mapData.map = buildMapConfig(null, result)
    mapData.total = area.chinaTotal
    mapData.today = area.chinaAdd
    mapData.table = area.areaTree[0].children
  }

    const xAxis = []
    const dataConfirm = []
    const dataSuspect = []
    const dataDead = []
    province_data.forEach(day=>{
      xAxis.push(day.ymd)
      dataConfirm.push(day.conNum)
      dataSuspect.push(day.cureNum)
      dataDead.push(day.deathNum)
    })

    mapData.chinaDayList = buildLineConfig(xAxis, dataConfirm, dataSuspect, dataDead)
  
  console.log(mapData)

  return mapData
}
