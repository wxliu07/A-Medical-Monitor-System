from flask import *
from utils import ServerConfig, Result
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import database
# import core.main
from werkzeug.utils import secure_filename

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


@app.route('/api/database/isUser', methods=['GET'])
def isUser():
    try:
        print("request: ", request)
        print("request.args", request.args)
        username = request.args.get('username')
        password = request.args.get('password')
        result = database.isUser(username, password)
        if result:
            print('查询成功')
            return Result.success("查询成功")
        else:
            print('查询失败')
            return Result.fail("不存在用户")
    except Exception as e:
        print(e)
        return Result.fail("查询失败")



@app.route('/api/database/isAdmin', methods=['GET'])
def isAdmin():
    try:
        database.isAdmin('liu', '123')
        return Result.success("获取成功")
    except Exception as e:

        print(e)
        return Result.fail("获取失败")


@app.route('/api/database/getAllUsers', methods=['GET'])
def getAllUsers():
    try:
        users = database.getAllUsers()
        if users is not None:
            return Result.success_data(data=users, info="用户成员获取成功")
        else:
            return Result.success(info="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")


@app.route('/api/database/getMonitorData', methods=['GET'])
def getMonitorData():
    try:
        uid = request.args.get("uid")
        datas = database.getMonitorData(uid=uid)
        if datas is not None:
            return Result.success_data(data=datas, info="获取监测数据成功")
        else:
            return Result.success(info="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")




@app.route('/api/database/getVideosData', methods=['GET'])
def getVideosData():
    try:
        uid = request.args.get("uid")
        datas = database.getVideos(uid=uid)
        if datas is not None:
            return Result.success_data(data=datas, info="获取视频数据成功")
        else:
            return Result.success(info="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")



@app.route('/api/uploadFile', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file is None:
        return jsonify({'message': "文件上传失败，未接收到文件"}), 400

    file_name = secure_filename(file.filename)
    if file_name == '':
        return jsonify({'message': "文件上传失败，文件名不合法"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)
    return Result.success("文件上传成功")





if __name__ == '__main__':
    # 启动Flask服务器
    app.run(debug=True)  # app.config['DEBUG'] = True 会是服务在起来的时候多起一个进程以便调试



