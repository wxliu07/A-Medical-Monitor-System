import threading
import uuid

from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import database
from utils import ServerConfig, Result

from core.main import *

serverConfig = ServerConfig()
app = Flask(__name__)
CORS(app)

# 静态文件
FILES_PATH = os.path.abspath(os.path.dirname(__file__)) + '/static'
if not os.path.exists(FILES_PATH):
    os.mkdir(FILES_PATH)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = serverConfig.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置为 True 时，启用修改追踪，会在对象更改时发出信号

# 初始化数据库
db = SQLAlchemy(app)

# 文件上传
UPLOAD_FOLDER_URL = os.path.abspath(os.path.dirname(__file__)) + '/static/videos/'  # 上传路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_URL

# 上传文件的拓展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'mp4', 'avi'}

# 存储任务状态和结果
tasks = {}


# 判断是否允许上传的类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


# 首页
@app.route('/')
def home():
    return redirect(url_for('static', filename='./index.html'))


# 上传视频
@app.route('/api/uploadFile', methods=['POST'])
def uploadFile():
    file = request.files.get('file')
    if file is None:
        return Result.fail(desc="文件上传失败，未接收到文件")
    file_name = secure_filename(file.filename)
    if file_name == '':
        return Result.fail(desc="文件上传失败，文件名不合法")
    if not allowed_file(file.filename):
        return Result.fail(desc="文件上传失败，不支持的文件类型")
    task_id = str(uuid.uuid4())  # 生成唯一id
    # 添加文件后缀名
    file_extension = file_name.rsplit('.', 1)[1].lower()  # 获取文件后缀名
    file_name = f"{task_id}.{file_extension}"  # 新的文件名

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)

    # 在新线程中启动处理
    thread = threading.Thread(target=process_file, args=(file_path, task_id, tasks))
    thread.start()

    return Result.success(data={"task_id": task_id}, desc="文件接收成功，开始处理")


# 获取文件处理状态
@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id: str):
    status, result = tasks.get(task_id, ("未知任务", None))
    if result is None:
        return Result.fail(desc="文件未处理完成")
    else:
        return Result.success(data={"status": status, "result": result}, desc="文件处理结束")


def process_file(file_path, task_id, task_dict):
    # Dummy processing logic
    # import time
    # time.sleep(5)  # Simulate a time-consuming task
    process_results = process_video(file_path=file_path, chunk_duration=15)
    for result in process_results:
        database.insertDatas(user_id=1, emotion=result['emotion'], rr=result['rr'],
                             hr=result['hr'], spo2=result['spo2'], time=result['time'])
    task_dict[task_id] = ("完成", {"result": process_results})  # Update the task status


# 判断是否为用户
@app.route('/api/database/isUser', methods=['GET'])
def checkIsUser():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        print("username: " + str(username))
        print("username: {}, password: {}".format(username, password))
        result = database.isUser(username, password)
        if result:
            print('查询成功')
            return Result.success(data=result, desc="查询成功")
        else:
            print('用户查询失败, 不存在用户')
            return Result.fail(desc="查询失败, 不存在此用户")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数有误")


# 判断是否为管理员
@app.route('/api/database/isAdmin', methods=['GET'])
def checkIsAdmin():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        print("username: {}, password: {}".format(username, password))
        result = database.isAdmin(username, password)
        if result:
            print('查询成功')
            return Result.success(data=result, desc="查询成功")
        else:
            print('管理员查询失败, 不存在此管理员')
            return Result.fail(desc="查询失败, 不存在此用户")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数有误")


# 获取所有用户基本信息
@app.route('/api/database/getAllUsers', methods=['GET'])
def getAllUsers():
    try:
        users = database.getAllUsers()
        if users is not None:
            return Result.success(data=users, desc="用户成员获取成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数异常")


@app.route('/api/database/getAllMonitorData', methods=['GET'])
def getAllMonitorData():
    try:
        datas = database.getAllMonitorData()
        if datas is not None:
            return Result.success(data=datas, desc="用户成员获取成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数异常")


@app.route('/api/database/getAllVideoData', methods=['GET'])
def getAllVideoData():
    try:
        videos = database.getAllVideoData()
        if videos is not None:
            return Result.success(data=videos, desc="用户成员获取成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数异常")


# 通过uid获取用户的检测信息
@app.route('/api/database/getMonitorDataByUid', methods=['GET'])
def getMonitorData():
    try:
        uid = request.args.get("uid")
        datas = database.getMonitorData(uid=uid)
        if datas is not None:
            return Result.success(data=datas, desc="获取监测数据成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")


# 通过uid获取用户的检测记录信息
@app.route('/api/database/getVideosDataByUid', methods=['GET'])
def getVideosData():
    try:
        uid = request.args.get("uid")
        datas = database.getVideos(uid=uid)
        if datas is not None:
            return Result.success(data=datas, desc="获取视频数据成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数异常")


# 通过uid获取用户的心率检测记录
@app.route('/api/database/getHrDataByUid', methods=['GET'])
def getHrDataByUid():
    try:
        uid = request.args.get("uid")
        datas = database.getHrByUid(uid=uid)
        if datas is not None:
            return Result.success(data=datas, desc="获取HR数据成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail(desc="参数异常")


# 通过uid获取用户的呼吸率检测记录
@app.route('/api/database/getRrDataByUid', methods=['GET'])
def getRrDataByUid():
    try:
        uid = request.args.get("uid")
        datas = database.getRrByUid(uid=uid)
        if datas is not None:
            return Result.success(data=datas, desc="获取呼吸率成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")


# 通过uid获取用户的血氧饱和度检测记录
@app.route('/api/database/getSpO2DataByUid', methods=['GET'])
def getSpO2DataByUid():
    try:
        uid = request.args.get("uid")
        datas = database.getSpO2ByUid(uid=uid)
        if datas is not None:
            return Result.success(data=datas, desc="获取血氧饱和度成功")
        else:
            return Result.success(desc="数据为空")
    except Exception as e:
        print(e)
        return Result.fail("参数异常")


if __name__ == '__main__':
    # 启动Flask服务器
    app.run(debug=True)  # app.config['DEBUG'] = True 会是服务在起来的时候多起一个进程以便调试
