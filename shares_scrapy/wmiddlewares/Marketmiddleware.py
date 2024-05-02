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
import time, random
from shares_scrapy.common.echo import echo, echo_info
from shares_scrapy.common.w_re import CleanData
import json


class Marketmiddleware(object):
    options = Options()  # 页头设置
    headless = True  # 无头模式
    url = ''  # 访问地址
    body = ''  # response 返回内容
    webdriver = webdriver
    handles = []
    total_crawl = 0

    def __init__(self):
        if self.headless:
            # 开启无头模式
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        self.options.add_argument("--no-sandbox")  # 沙盒模式
        self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        self.options.add_argument('log-level=3')    # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
        }
        self.options.add_experimental_option('prefs', prefs)
        self.driver = self.webdriver.Chrome(options=self.options)  # 启动chromedriver
        echo('打开默认网址')
        self.driver.get('https://finance.sina.com.cn/realstock/company/sz002594/nc.shtml')
        self.handles.append(self.driver.current_window_handle)
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/a[3]').click()
        self.handles.append(self.driver.current_window_handle)

    def process_request(self, request, spider):
        self.total_crawl += 1
        # 第二个handle获取数据
        time.sleep(random.randint(10, 18))
        if self.total_crawl % 10 == 0:
            echo_info('downloadmiddleware','每10次停留2分钟')
            time.sleep(20)
        echo_info('downloadmiddleware', 'download->'+request.url)
        self.driver.switch_to.window(self.driver.window_handles[1])             # 切换到最后一个handle
        self.driver.get(request.url)
        compress_data = CleanData(self.driver.page_source)                      # 获取压缩JS文件

        # 清洗数据
        compress_data.delete_html()
        compress_data.to_compress()
        just_data = compress_data.result_string.split('"')

        # 组装JS
        load_js = self.get_js('sina_h5k.js')                                    # 获取要执行的JS
        new_js = load_js.replace('{compress}', just_data[1])

        # 回到第一个handle执行JS函数
        self.driver.switch_to.window(self.driver.window_handles[0])             # 切换会第二个handles
        stack_data = self.driver.execute_script(new_js)                      # 在源文件中执行JS
        json_str = json.dumps(stack_data)
        echo_info('downloadmiddleware', 'download 成功')
        return HtmlResponse(body=json_str, encoding='utf-8', request=request,
                            url=str(self.url))

    def process_spider_closed(self, spider, reason):
        echo("执行关闭driver")
        self.driver.close()
        self.driver.quit()

    def get_js(self, js_name):
        with open('E:/wooght-server/scripy_wooght//shares_scrapy/shares_scrapy/wmiddlewares/js/'+str(js_name), 'r') as file:
            js_code = file.read()
        return js_code
