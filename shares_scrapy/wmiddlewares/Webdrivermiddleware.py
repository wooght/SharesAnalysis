# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Webdrivermiddleware.py
@Author     :wooght
@Date       :2024/5/27 10:27
@Content    :webdriver 中间件基类
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import redis

class WebdriverMiddleware(object):
    driver = None  # chrome driver
    options = webdriver.ChromeOptions()  # chrome options
    exception = None  # 报错标题
    e = None  # 报错内容
    current_ip = ''  # 当前代理IP
    headless = True  # 默认无头模式

    def __init__(self, is_proxy=False, maxtime=6, cookie_name=''):
        self.is_proxy = is_proxy  # 是否代理
        self.maxtime = maxtime  # timeout 最大时间
        self.cookie_name = cookie_name
        if len(self.cookie_name) > 0:
            pool = redis.ConnectionPool(host='192.168.101.103', port=6379, db=0, socket_connect_timeout=2, decode_responses=True)
            self.r = redis.Redis(connection_pool=pool)
            self.cookies = self.r.hgetall(self.cookie_name)
            """
                cookies:{key:value,key:value,...}
            """

    def set_option(self):
        """
            启动加载时调用(默认调用,以便后续直接访问url)
            设置属性及代理判断
        """
        if self.headless: self.options.add_argument("--headless")  # 无头模式
        self.options.add_argument("--disable-gpu")  # 禁止GPU加速
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        # self.options.add_argument('--incognito')  # 无痕模式
        self.options.add_argument('--disable-infobars') # 禁止提示自动化运行
        self.options.add_argument('--hide-scrollbars')  # 隐藏滚动条
        self.options.add_argument("--lang=zh_CN.UTF-8")  # 编码
        self.options.add_argument("--no-sandbox")  # 禁止沙盒模式
        # self.options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片
        self.options.add_argument('--log-level=0')  # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        self.options.add_argument('--appinfo=retail-admin')
        self.options.add_argument('--no-first-run')     # 禁止首次运行向导
        self.options.add_argument(f'--header=Sec-Fetch-Mode:cors')
        self.options.add_argument(f'--header=appinfo:retail-admin')
        self.options.add_argument(f'--header=Sec-Fetch-Dest:empty')
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
            # "profile.default_content_settings.fetch_dest": "empty",
            # "profile.default_content_settings.fetch_mode": "cors",
            # "profile.default_content_settings.fetch_site": "same-origin",
        }
        self.options.experimental_options['prefs'] = prefs
        # self.options.add_experimental_option('prefs', prefs)
        self.options.add_experimental_option('detach', True)  # 保持打开状态
        # 以下两个方法 屏蔽浏览器页头:自动化测试控制
        self.options.add_experimental_option('useAutomationExtension', False)  # 停用开发者模式
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # self.options.add_argument('--process-per-site')                       # 一个站点,一个进程
        if self.is_proxy: self.set_proxy()
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(self.maxtime)

    def set_proxy(self):
        """
            在is_proxy为False下,要设置代理,调用set_option()之前调用set_proxy()
        """
        if len(self.current_ip) > 0:
            proxy_str = '--proxy-server=http://{}'.format(self.current_ip)
            self.options.add_argument(proxy_str)

    def get_url(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            self.e = e
            self.exception = type(e).__name__
            return False

    def close_driver(self):
        self.driver.close()     # 关闭当前handle
        self.driver.quit()      # 退出webdriver

    def load_time(self, url):
        """
        测试访问时间,代理性能测试
        :param url:
        :return:load times
        """
        s = time.time()
        page = self.get_url(url)
        end = time.time()
        return (end - s) if page else page

    def new_window(self):
        """
        打开新的handle
        :return:None
        """
        self.driver.execute_script('window.open("")')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def set_cookies(self, cookies):
        """
        设置webdriver的新cookie
        :param cookies: dict {key:value, key:value,...}
        :return: None
        """
        for key, value in cookies.items():
            print(key, '|', value)
            self.driver.add_cookie({'name':key.strip(), 'value':value.strip()})

    def get_cookies(self):
        """
        获取webdriver的cookies
        :return: [{domain:,expiry:,name:,value:,path:,httpOnly:,..},{},{}...]
        """
        cookies = self.driver.get_cookies()     # get_cookies('cookie name') 获取单个cookie的值
        return cookies

    def save_cookies(self, cookies):
        """
        保存cookie到redis
        :param cookies: webdriver get到的cookie格式:[{},{},...]
        :return:None
        """
        cookie_temp = {}
        for cookie in cookies:
            self.r.hset(self.cookie_name, key=cookie['name'], value=str(cookie['value']))
            cookie_temp[cookie['name']] = cookie['value']
        # 当前新cookie
        self.cookies = cookie_temp

    def get_headers(self):
        """
        JS获取当前WEB的headers
        :return:
        """
        current_headers = self.driver.execute_script("return document.documentElement.outerHTML;")
        return current_headers

    def delay(self, s):
        time.sleep(s)


if __name__ == '__main__':
    web = WebdriverMiddleware()
    web.headless = False
    web.set_option()
    load_time = web.load_time('http://www.baidu.com')
    print(load_time)
    # request = web.driver.requests
    # for i in request:
    #     print(i.url)
    #     print(i.response.headers)
    # web.new_window()