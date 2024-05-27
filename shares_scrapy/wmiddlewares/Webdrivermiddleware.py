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
    options = Options()  # chrome options
    exception = None  # 报错标题
    e = None  # 报错内容
    current_ip = ''  # 当前代理IP
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TitansX/11.11.15 KNB/1.0 iOS/17.4.1 App/(null)/1.18.8 meituangroup/com.meituan.erp.retail.admin/1.18.8 meituangroup/1.18.8 WKWebView'
    headless = True  # 默认无头模式

    def __init__(self, is_proxy=False, maxtime=6, cookie_name=''):
        self.is_proxy = is_proxy  # 是否代理
        self.maxtime = maxtime  # timeout 最大时间
        self.cookie_name = cookie_name
        if len(self.cookie_name):
            pool = redis.ConnectionPool(host='192.168.101.103', port=6379, db=0, socket_connect_timeout=2, decode_responses=True)
            self.r = redis.Redis(connection_pool=pool)
            self.cookies = self.r.hgetall(self.cookie_name)

    def set_option(self):
        """
            启动加载时调用(默认调用,以便后续直接访问url)
            设置属性及代理判断
        """
        if self.headless: self.options.add_argument("--headless")  # 无头模式
        self.options.add_argument("--disable-gpu")  # 禁止GPU加速
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        # self.options.add_argument('--incognito')  # 无痕模式
        self.options.add_argument('disable-infobars') # 禁止提示自动化运行
        self.options.add_argument('--hide-scrollbars')  # 隐藏滚动条
        self.options.add_argument("lang=zh_CN.UTF-8")  # 编码
        self.options.add_argument("--no-sandbox")  # 禁止沙盒模式
        self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        self.options.add_argument('log-level=0')  # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        self.options.add_argument('--appinfo=retail-admin')
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
        self.options.add_experimental_option('useAutomationExtension', False)  # 停用开发者模式
        self.options.add_argument("--user-agent={}".format(self.user_agent))  # user-agent
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

    def delay(self, s):
        time.sleep(s)

if __name__ == '__main__':
    web = WebdriverMiddleware()
    web.headless = False
    web.set_option()
    load_time = web.load_time('http://www.baidu.com')
    print(load_time)
    web.new_window()
    time.sleep(3)
    print(web.driver.window_handles)
    cookie_strs = 'erp-bsid=AbCxTzhGH4i49CoHVIVJjBOIjNLwM1gKkHpUtPiFKHr9KyoFSOTaZ3H5JoE4car3iSURP2hbWbC4Zz2AYIErLA; retail-poiid=163134577; retailadmin-app-native-version=1.18.8; retailadmin-app-version=1.1.0; username=wooght; network=unknown; WEBDFPID=z936y4z9u3w25u1117282v2x0uwuyx2y810wwzu75xy9795840wz4z50-2007001390280-1691641389695QASWOMA868c0ee73ab28e1d0b03bc83148500062862; _utm_content=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; cityid=0; dpid=; uuid=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; __mta=217291049.1678035125091.1716793585867.1716793618960.5637; pos_brand=MEITUAN; token-for-cors=AbCxTzhGH4i49CoHVIVJjBOIjNLwM1gKkHpUtPiFKHr9KyoFSOTaZ3H5JoE4car3iSURP2hbWbC4Zz2AYIErLA; _lxsdk_s=18fb745f352-421-25c-90e%7C%7CNaN; appId=3; biz_acct_id=46999744; login_token=uGw6tO4UR0uEWCMvJTVs0wCJeEPvsrheHja2I9_AgU4XNFZEzHCrM1GdZKNh2hHbKJEvsfYcayW01Va63ATSsw; _lxsdk=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; _lxsdk_cuid=186b2b00354c8-0ca39813e3bcf4-693b7b53-505c8-186b2b00354c8; _lxsdk_unoinid=183f2b1959f4472b92bf813928b4498ba164619479778148387'
    cookie_temp = cookie_strs.split('; ')
    cookie_dict = {}
    for cookie in cookie_temp:
        current_cookie = cookie.split('=')
        cookie_dict[current_cookie[0]] = current_cookie[1]
    print(cookie_dict)
    web.get_url('https://www.meituan.com/')
    response_cookie = web.get_cookies()
    print(response_cookie)
    time.sleep(5)
    web.set_cookies(cookie_dict)
    web.driver.get('https://retailadmin-erp.meituan.com/api/order/queryOrder')
    # web.driver.refresh()    # 刷新
    refresh_cookies = web.get_cookies()
    print(refresh_cookies)
    # web.close_driver()

"""
erp-bsid=ZZhASTJsbdfv_HKnGubGVt8KI_6af9YcVur7ZDz4gfHMXrh-Wse1WQtxrnCsoR-kaGKo2V_oTfbDLxST8z9rGA; retail-poiid=163134577; retailadmin-app-native-version=1.18.8; retailadmin-app-version=1.1.0; username=wooght; WEBDFPID=z936y4z9u3w25u1117282v2x0uwuyx2y810wwzu75xy9795840wz4z50-2007001390280-1691641389695QASWOMA868c0ee73ab28e1d0b03bc83148500062862; __mta=217291049.1678035125091.1716787256251.1716787276122.5629; _utm_content=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; cityid=0; dpid=; network=unknown; uuid=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; _lxsdk_s=18fb745f352-421-25c-90e%7C%7CNaN; appId=3; biz_acct_id=46999744; login_token=ZZhASTJsbdfv_HKnGubGVt8KI_6af9YcVur7ZDz4gfHMXrh-Wse1WQtxrnCsoR-kaGKo2V_oTfbDLxST8z9rGA; pos_brand=MEITUAN; token-for-cors=ZZhASTJsbdfv_HKnGubGVt8KI_6af9YcVur7ZDz4gfHMXrh-Wse1WQtxrnCsoR-kaGKo2V_oTfbDLxST8z9rGA; _lxsdk=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; _lxsdk_cuid=186b2b00354c8-0ca39813e3bcf4-693b7b53-505c8-186b2b00354c8; _lxsdk_unoinid=183f2b1959f4472b92bf813928b4498ba164619479778148387
"""