# 请开发时终端输入：set FLASK_ENV=development（windows系统下）
# flask version：2.1.3
# reference：https://tutorial.helloflask.com/
from flask import Flask,render_template
app = Flask(__name__)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

#注册一个处理函数(不是装饰器)，即视图函数 用户访问对应url就会触发对应函数
#如果我们这里定义的 URL规则是/hello，那么完整 URL 就是 http://localhost:5000/hello
#服务器获得函数返回值然后返给浏览器 后者接受相应把值显示出来
@app.route('/')  
def index():
    return render_template('index.html',name=name,movies=movies)
    
if __name__ == "__main__":
    print(__name__)
    #app.run(host='127.0.0.1', port=8080)