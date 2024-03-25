from flask import Flask
from utils import ServerConfig, Result
from flask_sqlalchemy import SQLAlchemy
import os
from database import Users

serverConfig = ServerConfig()
app = Flask(__name__)

# 静态文件
FILES_PATH = os.path.abspath(os.path.dirname(__file__)) + '/static'
if not os.path.exists(FILES_PATH):
    os.mkdir(FILES_PATH)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = serverConfig.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True   # 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置为 True 时，启用修改追踪，会在对象更改时发出信号

# 初始化数据库
db = SQLAlchemy(app)


@app.route('/')  # 代表首页
def hello_world():
    try:
        users = Users(username='xiao-wang', password='3333', age=11, gender='男', phone='111111')
        db.session.add(users)
        db.session.commit()
        return Result.success("数据插入成功")
    except Exception as e:
        db.session.rollback()   # 数据回滚
        print(e)
        return Result.fail("数据插入失败")


@app.route('/getUserById', method=['GET'])
def get_user_by_id():
    try:

        return Result.success("获取成功")
    except Exception as e:

        print(e)
        return Result.fail("获取失败")

@app.route('/getAdminsById', method=['GET'])
def get_user_by_id():
    try:

        return Result.success("获取成功")
    except Exception as e:

        print(e)
        return Result.fail("获取失败")



if __name__ == '__main__':
    # 启动Flask服务器
    app.run(debug=True)  # app.config['DEBUG'] = True 会是服务在起来的时候多起一个进程以便调试


