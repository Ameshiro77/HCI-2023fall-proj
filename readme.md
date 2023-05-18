前端代码在client  用vue编写
后端代码在server 用flask框架搭建

目前进度：0.0000001%
# 疫情数据爬取接口:
1. [新浪接口](https://interface.sina.cn/news/wap/fymap2020_data.d.json):还在更新中,仅历史数据不再更新
2. [腾讯接口](https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5):数据类型很全,但不更新了
3. [具体省份接口](https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=province&province=beijing&&callback=beijingChartData):爬取网页数据后发现爬取省份信息方式,统一截止到12.20号