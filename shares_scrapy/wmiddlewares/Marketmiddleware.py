# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Marketmiddleware.py
@Author     :wooght
@Date       :2024/4/29 15:16
@Content    :行情下载中间件
"""
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, re
from shares_scrapy.common.echo import echo


class Marketmiddleware(object):
    options = Options()  # 页头设置
    headless = True  # 无头模式
    url = ''  # 访问地址
    body = ''  # response 返回内容
    webdriver = webdriver
    handles = []

    def __init__(self):
        if self.headless:
            # 开启无头模式
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        self.options.add_argument("--no-sandbox")  # 沙盒模式
        self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
        }
        self.options.add_experimental_option('prefs', prefs)
        self.driver = self.webdriver.Chrome(options=self.options)  # 启动chromedriver
        echo('打开默认网址:')
        self.driver.get('https://finance.sina.com.cn/realstock/company/sz002594/nc.shtml')
        self.handles.append(self.driver.current_window_handle)
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/a[3]').click()
        self.handles.append(self.driver.current_window_handle)

    def process_request(self, request, spider):
        time.sleep(2)
        self.driver.switch_to.window(self.handles[-1])          # 切换到最后一个handle
        self.driver.get(request.url)
        compress_data = self.driver.page_source                 # 获取压缩JS文件

        just_data = self.compress_split(compress_data)
        load_js = self.get_js('sina_h5k.js')
        load_js.replace('{compress}', just_data[1])

        compress_data = self.driver.execute_script(load_js)
        time.sleep(1)
        echo(compress_data)
        return HtmlResponse(body=compress_data, encoding='utf-8', request=request, url=str(self.url))

    def process_spider_closed(self, spider, reason):
        echo("执行关闭driver")
        self.driver.close()
        self.driver.quit()

    def get_js(self, js_name):
        with open('E:/wooght-server/scripy_wooght//shares_scrapy/shares_scrapy/wmiddlewares/js/'+str(js_name), 'r') as file:
            js_code = file.read()
        return js_code

    def compress_split(self, data):
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', data)
        new_data = text.replace(' ', '')
        new_data = new_data.replace('\n', '')
        just_data = new_data.split('"')
        return just_data
