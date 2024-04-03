import shutil
from flask import *
from utils import ServerConfig, Result
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import datetime
from database import Users
# import core.main

serverConfig = ServerConfig()
app = Flask(__name__)
CORS(app)

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

# 文件上传
UPLOAD_FOLDER_URL = os.path.abspath(os.path.dirname(__file__)) + '/static/videos/'  # 上传路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_URL

# 上传文件的拓展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'mp4'}
def is_allowed_file(filename: str) ->bool:
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/')  # 代表首页
def home():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/api/database/getUserById', methods=['GET'])
def get_user_by_id():
    flag = False
    if flag:
        try:

            return Result.success("测试成功")
        except Exception as e:

            print(e)
            return Result.fail("测试失败")
    else:
        return Result.fail("测试失败")




@app.route('/api/database/getAdminsById', methods=['GET'])
def get_admin_by_id():
    try:

        return Result.success("获取成功")
    except Exception as e:

        print(e)
        return Result.fail("获取失败")



@app.route('/api/uploadFile', methods=['POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    print(file)
    if file:
        # 保存文件
        src_path = app.config['UPLOAD_FOLDER']
        file.save(os.path.abspath(os.path.dirname(__file__)))

        # 临时文件用于得到信息
        shutil.copy(src_path, './temp') # 复制文件

        # temp_file_path = os.path.join('./temp', file.filename)
        # emotion = core.main.get_emotion(temp_file_path)

        return Result.success("获取成功")
    return Result.fail("获取失败")



def insertUser(user_name, user_password, user_age, user_gender, user_phone):
    try:
        users = Users(username=user_name, password=user_password, age=user_age, gender=user_gender, phone=user_phone)
        db.session.add(users)
        db.session.commit()
        return Result.success("获取成功")
    except Exception as e:
        db.session.rollback()  # 数据回滚
        print(e)
        return Result.fail("获取失败")


if __name__ == '__main__':
    # 启动Flask服务器
    app.run(debug=True)  # app.config['DEBUG'] = True 会是服务在起来的时候多起一个进程以便调试



