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
    num_file=f'results/results_num/{province_name}.csv'
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

#================================================#
#                 主 函 数 入 口                 #
#================================================#
@app.route("/")
def main():
    return render_template('index.html', name='index')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
