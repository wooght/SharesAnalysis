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
    insert_list = []
    exists_ip = all_proxy()
    for ip in ips:
        if ip in exists_ip: continue
        insert_list.append({'ip':ip, 'enabled':True})
    i = proxy_sitory.insert()
    r = connect.execute(i, insert_list)
    return r.rowcount


def all_proxy():
    s = proxy_sitory.select().where(proxy_sitory.c.enabled==True)
    r = connect.execute(s)
    return [row.ip for row in r.fetchall()]


def delete_ips():
    s = proxy_sitory.delete().where(proxy_sitory.c.enabled==False)
    r = connect.execute(s)
    return r.rowcount


def set_unenabled(ip):
    u = proxy_sitory.update().where(proxy_sitory.c.ip==ip).values(enabled=False)
    r = connect.execute(u)
    connect.commit()
    return r.rowcount