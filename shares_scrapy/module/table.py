# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :table.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :数据库模型
"""

from ..common.SecretCode import Wst
from sqlalchemy import Integer, String, Float
from sqlalchemy import create_engine, Table, Column, MetaData

host = '127.0.0.1'
port = '3306'
database = 'shares_scrapy'
user = 'root'
password = Wst.decryption('}a,>aN4|Y,9xODC0HUwq%.*T7<]+7}B>{P$>x')
db_uri = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'
engine = create_engine(db_uri,echo=False)               # 创建数据库引擎
connect = engine.connect()                              # 引擎与数据库握手连接
metadata = MetaData()


csrcclassify = Table('csrcclassify', metadata,
                     Column('id', Integer(), primary_key=True, autoincrement=True),
                     Column('name', String()),
                     Column('parent_id', Integer(), default=0),
                     Column('sina_code', String()))


area = Table('area', metadata,
             Column('id', Integer(), primary_key=True, autoincrement=True),
             Column('name', String()),
             Column('sina_code', String()))