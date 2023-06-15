# 运行此函数以搭建后端，提供api。
# ==================================
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import *
from werkzeug.utils import secure_filename
import pandas as pd
# ==================================



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__,
            static_folder="./template",
            template_folder="./template",
            static_url_path="")
CORS(app, supports_credentials=True)  # 跨域
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()
"""
return:
    confirmed:list of the predict result of confirmed
    num:list of the predict result of num
"""
def getData(province_name):
    confirmed_file=f'results/results_confirmed/{province_name}.csv'
    num_file=f'results/results_num/{province_name}_num.csv'
    confirmed = pd.read_csv(confirmed_file)
    confirmed  = confirmed .values.tolist()
    num = pd.read_csv(num_file)
    num  = num .values.tolist()
    date = "2022.1.2"
    res=[confirmed,num,date]
    return res

#================================================#
#                 以下是对API的定义               #
#================================================#

"""
用于根据 现有数据 输入模型 返回结果
"""
@app.route('/predict', methods=['GET'])
def predict():
    name = request.values.get('province_name')  # 前端传一个省份名字的参数
    # ========= 修改部分 ========== #
    data = getData(name)   # 需要自定义getData函数，根据城市名，传递一个数组：该数组包含这个城市的预测值（也可以加上已有值）
    return jsonify(data)

"""
根据四个人数数据 确定严重程度和医疗建议
"""
@app.route('/advice', methods=['GET'])
def advice():
    confirm = request.values.get('confirm')
    print("==========",type(confirm),confirm)
    suspect = request.values.get('suspect')
    heal = request.values.get('heal')
    dead = request.values.get('dead')
    # cf_a = 20520/31
    # sp_a = 23214/31
    per = (0.6 * int(confirm) / 20520.0) + (0.4 * int(suspect) / 23214.0)
    classify = ''
    advice = ''
    if per < 0.005:
        classify = '比较轻微'
        advice = "当前疫情程度较轻微，建议大家继续保持良好的个人卫生习惯。请经常洗手，使用洗手液或肥皂，尤其在接触公共场所后或打喷嚏、咳嗽后。同时，佩戴口罩有助于减少病毒传播，特别是在人群密集的地方。避免不必要的聚集和旅行，尽量在户外保持社交距离。关注当地卫生部门的指导和最新疫情信息，确保获取准确可靠的消息来源。"
    elif per < 0.01:
        classify = '轻微'
        advice = "当前疫情程度为轻微，但仍需保持警惕。请坚持良好的个人卫生习惯，包括经常洗手、佩戴口罩。尽量避免接触潜在传播源，遵守当地卫生部门的指引和规定。减少外出，特别是人群聚集的场所。如果出现不适症状，应及时就医并告知医生最近的活动历史。密切关注疫情动态，遵循专家和当地卫生部门的建议。"
    elif per < 0.05: 
        classify = '中度'
        advice = "当前疫情程度为中度，建议加强防护措施。请严格遵守卫生规范，如勤洗手、佩戴口罩。减少外出和接触他人，尽量居家工作。遵循医疗专家的建议，如有不适症状应及时就医，并遵守治疗方案。注意与家人保持良好的卫生习惯，避免共用个人物品。关注疫情信息更新，密切配合当地卫生部门的指示。"
    elif per < 0.1: 
        classify = '较为严重'
        advice = "当前疫情程度比较严重，需要加强防护措施。请高度警惕，严格遵守卫生规范，如勤洗手、佩戴口罩。限制社交接触，避免不必要的出行，尽量居家工作。关注疫情信息更新，及时获取准确的消息来源。配合政府和卫生部门的指示，遵守防疫措施，如隔离、检测等，以保护自己和他人的健康。"
    elif per < 0.15: 
        classify = '严重'
        advice = "当前疫情程度比较严重，需要加强防护措施。请高度警惕，严格遵守卫生规范，如勤洗手、佩戴口罩。限制社交接触，避免不必要的出行，尽量居家工作。关注疫情信息更新，及时获取准确的消息来源。配合政府和卫生部门的指示，遵守防疫措施，如隔离、检测等，以保护自己和他人的健康。"
    else:
        classify = '非常严重'
        advice = "当前疫情程度非常严重，请立即采取紧急措施保护自己和他人。严格遵守防护措施，包括频繁洗手、全面佩戴口罩，避免与他人近距离接触。避免不必要的社交活动和出行，尽量居家工作。严格遵守医疗专家的治疗方案。紧急时刻，密切关注疫情动态，遵从政府和卫生部门的紧急指示和命令。团结合作，共同努力，共渡难关。"
    return jsonify({"classify":classify,"advice":advice})


    
#================================================#
#                 主 函 数 入 口                 #
#================================================#
@app.route("/")
def main():
    return render_template('index.html', name='index')


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8081)
