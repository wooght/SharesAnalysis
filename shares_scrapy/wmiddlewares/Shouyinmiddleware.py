# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Shouyinmiddleware.py
@Author     :wooght
@Date       :2024/5/26 20:10
@Content    :美团收银中间件
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from shares_scrapy.common.SecretCode import Wst
import time
from shares_scrapy.common.w_re import CleanData
class ShouyinMiddleWare:
    index_url = 'http://dpurl.cn/TAaQoHkz'
    options = Options()
    driver = None
    sy_user = 'wooght'
    sy_password = Wst.decryption('8kkz=YAii=2HV961V8p-7D[-l')
    sy_code = '7370902'
    clearn_data = CleanData('')

    def __init__(self):
        self.set_option()

    def set_option(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        self.options.add_argument("lang=zh_CN.UTF-8")  # 编码
        self.options.add_argument("--no-sandbox")  # 沙盒模式
        self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        self.options.add_argument('log-level=3')  # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
        }
        self.options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(6)
        if self.get_url(self.index_url):
            print(self.driver.page_source)
            print('ShouyinMiddleWare开启成功')
            # 进入iframe
            src = self.driver.find_element(By.XPATH, '/html/body/section/iframe').get_attribute('src')
            # self.driver.switch_to.frame(0)
            self.get_url(src)
            time.sleep(2)
            self.driver.find_element(By.ID, 'part_key').send_keys(self.sy_code)
            self.driver.find_element(By.ID, 'login').send_keys(self.sy_user)
            self.driver.find_element(By.ID, 'password').send_keys(self.sy_password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
            time.sleep(2)
            print(self.driver.page_source)
            self.driver.save_screenshot('common/pic/shouyinresult.png')
            print('登录成功' if '商品' in self.driver.page_source else '登录失败')
            self.driver.switch_to.parent_frame()
        else:
            raise IgnoreRequest('访问失败{}'.format(self.index_url))

    def process_request(self, request, spider):
        print('访问spider:{}提供的URL:{}'.format(spider.name, request.url))
        page = self.get_url(request.url)
        if page:
            print(self.driver.page_source)
            self.clearn_data.result_string = self.driver.page_source
            self.clearn_data.delete_html()
            return HtmlResponse(body=self.clearn_data.result_string, encoding='utf-8', request=request, url=request.url)
        else:
            raise IgnoreRequest('访问失败{}'.format(request.url))



    def get_url(self,url):
        print("尝试打开地址{}".format(url))
        try:
            self.driver.get(url)
            # WebDriverWait(self.driver, 10).until(presence_of_element_located((By.XPATH, '/html/head/title')))
            # print(self.driver.execute_script("return {httpStatus: document.httpStatus, status: document.status};"))
            return True
        except Exception as e:
            print(f'.....错误{type(e).__name__}....')
            print(e)
            return False