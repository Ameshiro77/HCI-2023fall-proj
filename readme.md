前端代码在client  用vue编写
后端代码在server 用flask框架搭建

目前进度：0.0000001%
# 疫情数据爬取接口:
1. [新浪接口](https://interface.sina.cn/news/wap/fymap2020_data.d.json):还在更新中,仅历史数据不再更新
2. [腾讯接口](https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5):数据类型很全,但不更新了
3. [具体省份接口](https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=province&province=beijing):爬取网页数据后发现爬取省份信息方式,统一截止到2022.12.20号,数据从2020.1.20开始统计
# json文件解析
1. all.json:包含全国信息,信息截止2022.12.20,包含全国疫情数据变化,在`historylist`中
2. province.json:包含各省份信息,使用时先使用build-data中`getProvince`函数抓取对应省份信息，具体变化数据在historylist键中

# 省份数据获取
1. 运行`node getProvince.js`命令,获取所有省份数据,并以csv的形式保存在server/data文件夹中
2. asymptomatic文件夹代表无症状感染人数,confirmed文件夹代表确诊感染人数,num文件夹代表前面两个加起来的和，表示每日感染人数
# 手势交互
1. 使用开源框架handtrack.js进行交互,从而实现手势识别交互
2. 目前是这样实现的,左右手和图像中心来判断,左手代表控制左图,右手代表控制右图,open张手代表图片扩大,closed握拳代表折线图缩小
4. 每帧识别后通过调整datazoom属性来进行缩放