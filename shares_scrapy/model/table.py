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

shares = Table('shares', metadata,
               Column('id', Integer(), primary_key=True, autoincrement=True),
               Column('symbol', String()),  # 股票代号
               Column('code', String(), index=True),  # 股票代码
               Column('name', String()),  # 名称
               Column('area_id', String()),  # 地域ID
               Column('csrc_id', Integer()),  # 证监会行业ID

               Column('new_price', Float()),  # 最新价格
               Column('min_price', Float()),  # 最低价格
               Column('max_price', Float()),  # 最高价格
               Column('open_price', Float()),  # 今开价格
               Column('last_price', Float()),  # 昨天价格
               Column('price_change', Float()),  # 价格变动
               Column('change_percent', Float()),  # 变动幅度

               Column('buy', Float()),  # 买入
               Column('sell', Float()),  # 卖出
               Column('amount', Float()),  # 成交额
               Column('volume', Float()),  # 成交量

               Column('mktcap', Float()),  # 总市值
               Column('nmc', Float()),  # 流通值
               Column('pb', Float()))  # 市净率

"""
创建数据库:
create table if not exists shares (
    id int primary key auto_increment,
    symbol varchar(32),
    code varchar(16),
    name varchar(32),
    area_id int(4),
    csrc_id int(4),
    new_price float(16),
    min_price float(16),
    max_price float(16),
    open_price float(16),
    last_price float(16),
    price_change float(16),
    change_percent float(16),
    buy float(16),
    sell float(16),
    volume float(16),
    mktcap float(16),
    nmc float(16),
    pd float(16)
)
"""