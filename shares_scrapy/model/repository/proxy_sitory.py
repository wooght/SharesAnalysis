# -- coding: utf-8 -
"""
@project    :scrapy_test
@file       :proxy_sitory.py
@Author     :wooght
@Date       :2024/5/3 23:34
@Content    :代理IP仓库
"""

from ..table import *

def add_proxy(ips):
    """
    添加代理IP
    :param ips:
    :return:
    """
    insert_list = []
    exists_ip = all_proxy()
    for ip in ips:
        if ip in exists_ip: continue
        insert_list.append({'ip':ip, 'enabled':True})
    i = proxy_sitory.insert()
    r = connect.execute(i, insert_list)
    return r.rowcount


def all_proxy():
    """
    获取代理IP
        enabled False 不获取
        islock True 不获取
    :return:
    """
    s = proxy_sitory.select().filter(proxy_sitory.c.enabled==True, proxy_sitory.c.islock==False)
    r = connect.execute(s)
    return [row.ip for row in r.fetchall()]


def delete_ips():
    """
        删除无用的IP
    :return:
    """
    s = proxy_sitory.delete().where(proxy_sitory.c.enabled==False)
    r = connect.execute(s)
    return r.rowcount


def set_unenabled(ip):
    """
        将无法访问的IP 设置为 enabled=False
    :param ip:
    :return:
    """
    u = proxy_sitory.update().where(proxy_sitory.c.ip==ip).values(enabled=False)
    r = connect.execute(u)
    connect.commit()
    return r.rowcount

def set_lock(ip):
    """
        正在使用的IP上锁
    :param ip:
    :return:
    """
    u = proxy_sitory.update().where(proxy_sitory.c.ip == ip).values(islock=True)
    r = connect.execute(u)
    connect.commit()
    return r.rowcount