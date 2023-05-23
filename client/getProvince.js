const axios = require('axios')
let pinyin = require('pinyin')
const fs = require('fs')

const request = axios.create({
  baseURL: 'https://view.inews.qq.com/g2',
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
});


function transformChinaData (provinces) {
  provinces.forEach(province => {

    province.children.forEach(city => {
      if (province.name === '北京' || province.name === '上海') {
        city.cityName = city.name + '区'
        province.pinyin = pinyin(province.name, { style: pinyin.STYLE_NORMAL }).join('')
      } else {
        if (province.name === '陕西') {
          province.pinyin = 'shanxi1'
          city.cityName = city.name + '市'
        } else if (province.name === '重庆') {
          province.pinyin = 'chongqing'
          city.cityName = city.name
        } else if (province.name === '西藏') {
          province.pinyin = 'xizang'
          city.cityName = city.name + '市'
        } else {
          province.pinyin = pinyin(province.name, { style: pinyin.STYLE_NORMAL }).join('')
          city.cityName = city.name + '市'
        }
      }
    })
    
  })

  // console.log(provinces)
}

function getData () {
  request.get('/getOnsInfo?name=disease_h5')
    .then(res => {
      console.log(res.data.data)
      return
      let rawData = JSON.parse(res.data.data)
      let provinces = rawData.areaTree[0].children

      transformChinaData (provinces)
      fs.writeFileSync('./src/data/area.json', JSON.stringify(rawData))
    })
}
//province:beijing or shanghai ..exmample
function getProvince(province){
  const req= axios.create({
    baseURL: 'https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=province&province='+province
  })
  req.get('')
  .then(res=>{
    rawData=res.data.data
    res=[];
    asympto=[];
    conums=[]
    //统一输入为1051向量,因为有些地区开始时间相差几天,不利于之后模型的训练
    for(let i=0;i<1050;i++){
        let mid=rawData['historylist'][i]['conadd']   //确诊新增
        let asymptomatic=rawData['historylist'][i]['locAsymNum']  //无症状新增
        x=parseInt(asymptomatic)
        if(x<0||String(x)=='NaN')x=0
        let conum=parseInt(mid)+x; //每日阳性新增
        res.push(mid);
        asympto.push(x);
        conums.push(conum);
    }
    res=res.reverse();
    asympto=asympto.reverse();
    conums=conums.reverse();
    console.log(`数组长度为${res.length}`);
    res = res.join('\n');
    conums = conums.join('\n');
    asympto = asympto.join('\n');
    fs.writeFile(`../server/data/confirmed/${province}_confirmed.csv`, res, 'utf8', (err) => {
        if (err) {
          console.error('写入文件时发生错误:', err);
        } else {
          console.log(`数据已成功写入到 ${province}.csv 文件`);
        }
    });
    fs.writeFile(`../server/data/asymptomatic/${province}_asymptomatic.csv`, asympto, 'utf8', (err) => {
      if (err) {
        console.error('写入文件时发生错误:', err);
      } else {
        console.log(`数据已成功写入到 ${province}.csv 文件`);
      }
    });
    fs.writeFile(`../server/data/num/${province}_num.csv`, conums, 'utf8', (err) => {
      if (err) {
        console.error('写入文件时发生错误:', err);
      } else {
        console.log(`数据已成功写入到 ${province}.csv 文件`);
      }
    });
  })
}
function getAll(){
  const req= axios.create({
    baseURL: 'https://interface.sina.cn/news/wap/fymap2020_data.d.json'
  })
  req.get('')
  .then(res=>{
    //let rawData = JSON.parse(res.data.replace(/^jsoncallback\(|\)\;/g, '')).data.list
    console.log(res.data)
    let rawData=res.data
    fs.writeFileSync('./src/data/a.json', JSON.stringify(rawData))
  })

}
const provinces = [
    'anhui', 'beijing', 'chongqing', 'fujian', 'gansu', 'guangdong', 'guangxi',
    'guizhou', 'hainan', 'hebei', 'heilongjiang', 'henan', 'hubei', 'hunan',
    'jiangsu', 'jiangxi', 'jilin', 'liaoning', 'neimenggu', 'ningxia',
    'qinghai', 'shanxis', 'shandong', 'shanghai','shanxi', 'sichuan', 'tianjin',
    'xizang', 'xinjiang', 'yunnan', 'zhejiang'
  ];
provinces.forEach(function(element){
    getProvince(element);
});
//getProvince('shanghai')
//getData()
