# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :GetProxy.py
@Author     :wooght
@Date       :2024/5/15 19:59
@Content    :获取代理IP, 基于已经挂载IP爬虫
"""
import sys, os

sys.path.append(os.path.dirname(__file__))

import redis
from mount import get_ips


class GetProxy:
    def __init__(self, name):
        """
        :param name:redis的key名
        """
        self.name = name
        pool = redis.ConnectionPool(host='192.168.101.103', port=6379, db=0, socket_connect_timeout=2)
        self.r = redis.Redis(connection_pool=pool)

    def add_ip(self, ips):
        """
        添加 IP
        :param ips:
        :return: 添加成功个数
        """
        ips = [ips] if isinstance(ips, str) else ips
        return self.r.sadd(self.name, *ips)

    def get_ip(self):
        """
        随机获取IP 如果传入旧的IP,则删除旧的IP
        :return: 新的IP或者False
        """
        if self.r.scard(self.name) < 2:
            get_ips.delay()
        ip = self.r.srandmember(self.name, 1)
        if len(ip) > 0:
            self.del_ip(ip[0])  # 取出后删除
            return ip[0].decode('utf-8')
        else:
            return False

    def del_ip(self, ip):
        """
        删除已经使用的IP
        :param ip:
        :return:
        """
        self.r.srem(self.name, ip)

    def set_empty(self):
        """
        删除全部IP
        :return:None
        """
        all_ips = self.r.smembers(self.name)
        for ip in all_ips:
            self.r.srem(self.name, ip)
