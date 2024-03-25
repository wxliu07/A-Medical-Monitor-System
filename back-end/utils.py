import json
import os
import configparser
from flask.json import JSONEncoder

# 数据库和服务器配置内容
class ServerConfig:
    def __init__(self):
        cfg = configparser.ConfigParser()
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.conf") # 配置文件地址
        cfg.read(file)  # 读取配置文件
        self.SERVER_IP = str(cfg.get("server", "SERVER_IP"))
        self.HTTP_PORT = str(cfg.get("server", "HTTP_PORT"))
        self.SQLALCHEMY_DATABASE_URL = str(cfg.get("server","SQLALCHEMY_DATABASE_URL"))


# 自定义json编码器
class MyJSONEncoder(JSONEncoder):
    def default(self, obj) -> any:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        # 对象类型
        if isinstance(obj, object):
            return obj.get_json()   # 需要自定义get_json方法, 涉及数据集类的操作
        return json.JSONEncoder.default(self, obj)

# 结果集和定义
class Result:
    @staticmethod
    def success(message):
        return json.dumps({'code': 200, 'message': message, 'info' : '执行成功'},   # 转json对象, cls指定自定义的json编码器
                          cls=MyJSONEncoder, ensure_ascii=False)        # ensure_ascii是指定是否需要ASCII编码
    @staticmethod
    def fail(message):
        return json.dumps({'code': 400, 'message': message, 'info' : '执行失败'},
                          cls=MyJSONEncoder, ensure_ascii=False)
