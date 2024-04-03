from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import Result, ServerConfig

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

serverConfig = ServerConfig()
my_engine = create_engine(serverConfig.SQLALCHEMY_DATABASE_URL)     # 创建连接数据库的引擎，session连接数据库需要
metadata = MetaData(bind=my_engine)
Base.metadata.create_all(my_engine)         # 创建表结构
Session = sessionmaker(bind=my_engine)      # 创建一个配置过的Session类



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


def findUser(user_name, pass_word):
    db_session = Session()  # 实例化一个session
    user = db_session.query(Users).filter(and_(Users.username == user_name, Users.password == pass_word)).first()
    db_session.close()
    if user is not None:
        print("查询结果：", user.username, user.password)
        return True
    return False


def findAdmin(admin_name, admin_word):
    db_session = Session()  # 实例化一个session
    user = db_session.query(Admins).filter(Admins.username == admin_name, Admins.password == admin_word).first()
    db_session.close()
    if user is not None:
        return true
    else: return false
