# 运行此函数以搭建后端，提供api。
# ==================================
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import *
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from tensorflow.python.platform import gfile
import PIL
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

def getData(province_name):
    pass

#================================================#
#                 以下是对API的定义               #
#================================================#

"""
用于根据 现有数据 输入模型 返回结果
"""
@app.route('/predict', methods=['GET'])
def predict():
    result = 'static/result'  # 结果放到/static/result
    if not gfile.Exists(result):  # 如果没有就开一个新的
        os.mkdir(result)
    shutil.rmtree(result)  # 先删除下面所有文件 也就是过往记录

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
