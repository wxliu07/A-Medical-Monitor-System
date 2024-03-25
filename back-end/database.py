from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

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
            'user_id' : self.user_id,
            'username' : self.username,
            'password' : self.password,
            'age' : self.age,
            'gender' : self.age,
            'phone' : self.phone
        }


# 管理员类
class Admins(Base):
    __tablename__ = "admins_info"
    admin_id = Column(INT, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def get_json(self):
        return {
            'admin_id' : self.admin_id,
            'username' : self.username,
            'password' : self.password,
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
            'data_id' : self.data_id,
            'user_id' : self.user_id,
            'emotion' : self.emotion,
            'hr' : self.hr,
            'rr' : self.rr,
            'spo2' : self.spo2,
            'time' : self.time
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
            'video_id' : self.video_id,
            'user_id' : self.user_id,
            'data_id' : self.data_id,
            'video_url' : self.video_url,
            'record_time' : self.record_time
        }