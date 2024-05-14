# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :redis_model.py
@Author     :wooght
@Date       :2024/5/14 22:53
@Content    :redis 操作
"""
import redis


class WooghtRedis:
    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.101.103', port='6379', db=0, socket_connect_timeout=2)   # 连接池
        self.r = redis.Redis(connection_pool=pool)

    def set(self, name, value):
        self.r.set(name, value)

    def get(self, name):
        try:
            return self.r.get(name)
        except:
            return False

Wredis = WooghtRedis()