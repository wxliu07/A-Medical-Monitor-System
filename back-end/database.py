from sqlalchemy import *
# from sqlalchemy.ext.declarative import declarative_base   # sqlalchemy 2.x 版本被弃用
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from utils import Result, ServerConfig
from datetime import datetime
Base = declarative_base()


# 用户类
class Users(Base):
    __tablename__ = "users_info"
    user_id = Column(INT, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    age = Column(INT)
    gender = Column(String(50), nullable=False, default="男")
    phone = Column(String(50), nullable=False)

    def get_json(self):
        return {
            'username': self.username,
            'password': self.password,
            'age': self.age,
            'gender': self.age,
            'phone': self.phone
        }


# 管理员类
class Admins(Base):
    __tablename__ = "admins_info"
    admin_id = Column(INT, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def get_json(self):
        return {
            'admin_id': self.admin_id,
            'username': self.username,
            'password': self.password,
        }


# 监测信息类
class Datas(Base):
    __tablename__ = "monitor_data"
    data_id = Column(INT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(INT)
    emotion = Column(String(50), nullable=False)
    hr = Column(Float, nullable=False)
    rr = Column(Float, nullable=False)
    spo2 = Column(Float, nullable=False)
    time = Column(DateTime(), nullable=False)

    def get_json(self):
        return {
            'emotion': self.emotion,
            'hr': self.hr,
            'rr': self.rr,
            'spo2': self.spo2,
            'time': str(self.time)
        }


# 视频记录类
class Video(Base):
    __tablename__ = "video_records"
    video_id = Column(INT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(INT)
    data_id = Column(INT)
    video_url = Column(String(50), nullable=False)
    record_time = Column(DateTime(), nullable=False)

    def get_json(self):
        return {
            'video_id': self.video_id,
            'user_id': self.user_id,
            'data_id': self.data_id,
            'video_url': self.video_url,
            'record_time': str(self.record_time)
        }


serverConfig = ServerConfig()
my_engine = create_engine(serverConfig.SQLALCHEMY_DATABASE_URL)  # 创建连接数据库的引擎，session连接数据库需要
Base.metadata.create_all(my_engine)  # 创建表结构
Session = sessionmaker(bind=my_engine)  # 创建一个配置过的Session类


def insertUser(db, user_name, user_password, user_age, user_gender, user_phone):
    try:
        users = Users(username=user_name, password=user_password, age=user_age, gender=user_gender, phone=user_phone)
        db.session.add(users)
        db.session.commit()
        return Result.success("插入成功")
    except Exception as e:
        db.session.rollback()  # 数据回滚
        print(e)
        return Result.fail("插入失败")


def insertDatas(user_id, emotion, hr, rr, spo2, time):
    try:
        db_session = Session()  # 实例化一个session
        data = Datas(user_id=user_id, emotion=emotion, hr=hr, rr=rr, spo2=spo2, time=time)
        # users = Users(username=user_name, password=user_password, age=user_age, gender=user_gender, phone=user_phone)
        db_session.add(data)
        db_session.commit()
        return Result.success("插入成功")
    except Exception as e:
        db_session.rollback()  # 数据回滚
        print(e)
        return Result.fail("插入失败")


def isUser(user_name, pass_word):
    if user_name is None or pass_word is None:
        return False  # 提前返回空字典，表示没有提供有效的认证信息
    db_session = Session()  # 实例化一个session
    user = db_session.query(Users).filter(and_(Users.username == user_name, Users.password == pass_word)).first()
    db_session.close()
    if user is not None:
        print("查询结果：", user.username, user.password)
        return True
    return False


def isAdmin(admin_name, admin_word):
    if admin_name is None or admin_word is None:
        return False  # 提前返回空字典，表示没有提供有效的认证信息
    db_session = Session()  # 实例化一个session
    user = db_session.query(Admins).filter(and_(Admins.username == admin_name, Admins.password == admin_word)).first()
    db_session.close()
    if user is not None:
        print("查询结果：", user.username, user.password)
        return True
    return False


def getAllUsers():
    db_session = Session()  # 实例化一个session
    users = db_session.query(Users).all()
    db_session.close()
    result = []
    if users is not None:
        for user in users:
            result.append(user.get_json())
    return result


def getAllMonitorData():
    db_session = Session()  # 实例化一个session
    videos = db_session.query(Datas).all()
    db_session.close()
    result = []
    if videos is not None:
        for video in videos:
            result.append(video.get_json())
    return result


def getAllVideoData():
    db_session = Session()  # 实例化一个session
    datas = db_session.query(Video).all()
    db_session.close()
    result = []
    if datas is not None:
        for data in datas:
            result.append(data.get_json())
    return result


def getMonitorData(uid):
    db_session = Session()  # 实例化一个session
    datas = db_session.query(Datas).filter(Datas.user_id == uid).all()
    db_session.close()
    result = []
    if datas is not None:
        for data in datas:
            result.append(data.get_json())
    return result


def getVideos(uid):
    db_session = Session()  # 实例化一个session
    datas = db_session.query(Video).filter(Video.user_id == uid).all()
    db_session.close()
    result = []
    if datas is not None:
        for data in datas:
            result.append(data.get_json())
    return result


def getHrByUid(uid):
    db_session = Session()  # 实例化一个session
    result = []
    try:
        heart_rate_info = db_session.query(Datas.hr, Datas.time) \
            .join(Users, Users.user_id == Datas.user_id) \
            .filter(Users.user_id == uid).all()
        for info in heart_rate_info:
            hr_data = {
                'hr': info.hr,
                'time': str(info.time)
            }
            result.append(hr_data)
    except Exception as e:
        print("错误: {}".format(e))
    finally:
        db_session.close()
    return result


def getRrByUid(uid):
    db_session = Session()  # 实例化一个session
    result = []
    try:
        rr_info = db_session.query(Datas.rr, Datas.time) \
            .join(Users, Users.user_id == Datas.user_id) \
            .filter(Users.user_id == uid).all()
        for info in rr_info:
            hr_data = {
                'rr': info.rr,
                'time': str(info.time)
            }
            result.append(hr_data)
    except Exception as e:
        print("错误: {}".format(e))
    finally:
        db_session.close()
    return result


def getSpO2ByUid(uid):
    db_session = Session()  # 实例化一个session
    result = []
    try:
        spo2_info = db_session.query(Datas.spo2, Datas.time) \
            .join(Users, Users.user_id == Datas.user_id) \
            .filter(Users.user_id == uid).all()
        for info in spo2_info:
            hr_data = {
                'spo2': info.spo2,
                'time': str(info.time)
            }
            result.append(hr_data)
    except Exception as e:
        print("错误: {}".format(e))
    finally:
        db_session.close()
    return result


if __name__ == '__main__':
    # print(isUser('liu', 123))
    insertDatas(1, 'happy', 86, 15, 98, datetime.now())
    # print(getSpO2ByUid(1))
