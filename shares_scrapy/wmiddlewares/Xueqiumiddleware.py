# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Xueqiumiddleware.py
@Author     :wooght
@Date       :2024/6/3 19:04
@Content    :雪球WEB中间件 登录
"""
from shares_scrapy.wmiddlewares.Webdrivermiddleware import WebdriverMiddleware
from selenium.webdriver.common.by import By
from shares_scrapy.common.SecretCode import Wst
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest
from selenium.webdriver.common.action_chains import ActionChains
from shares_scrapy.common.yzm_xueqiu import move_pixel
import random
from scrapy import signals
import time

class XueqiuMiddleware(WebdriverMiddleware):
    xueqiu_name = Wst.decryption('!6W9m2,[$:;D$E9]/#IMB%,x};?bK3=W0Z+%.{=$C{=')
    xueqiu_password = Wst.decryption('8kkz=YAii=2HV961V8p-7D[-l')
    headless = False
    index_url = 'https://xueqiu.com/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

    def __init__(self,  is_proxy=False, maxtime=6, cookie_name='xueqiu'):
        super().__init__(is_proxy, maxtime, cookie_name)
        self.set_option()

    @classmethod
    def from_crawler(cls, crawler):
        print('加载XueqiuMiddleware')
        s = cls()
        crawler.signals.connect(s.process_spider_closed, signals.engine_stopped)
        return s

    def set_option(self):
        super().set_option()
        page = self.get_url(self.index_url)
        if page:
            if len(self.cookies) > 0:
                self.set_cookies(self.cookies)
                self.delay(2)
                self.get_url(self.index_url)
                self.delay(5)
                if '我的首页' in self.driver.page_source:
                    print('cookie 成功登录')
                    return
            self.delay(2)
            # 点击密码登录
            self.driver.find_element(By.XPATH, '//*[@id="modal__login__main"]/div[1]/div[1]/div[1]/a[2]').click()
            # 输入内容
            self.driver.find_element(By.XPATH, '//*[@id="modal__login__main"]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(self.xueqiu_name)
            self.driver.find_element(By.XPATH, '//*[@id="modal__login__main"]/div[1]/div[1]/div[2]/form/div[2]/input').send_keys(self.xueqiu_password)
            self.driver.find_element(By.XPATH, '//*[@id="modal__login__main"]/div[2]/label/i').click()
            self.delay(2)
            # 点击登录按钮
            self.driver.find_element(By.XPATH, '//*[@id="modal__login__main"]/div[2]/div[2]').click()
            self.delay(3)
            self.write_yzm()
        else:
            print('打开失败')

    def write_yzm(self):
        # self.driver.set_window_size(300, 400)
        pic_name = random.randint(10000, 99999)
        self.driver.save_screenshot('common/pic/xueqiu/{}.png'.format(str(pic_name)))
        self.delay(2)
        # 获取移动的距离 单位像素 分别率放大了1.5倍
        distance = int(move_pixel(pic_name) / 1.5)
        print(distance)
        # 每次移动10px,移动整数次
        move_second = distance // 10
        last_distance = distance % 10
        # 设置回正常分辨率
        # self.driver.set_window_size(1600, 900)
        # 点击移动按钮
        move_button = self.driver.find_element(By.CLASS_NAME, 'geetest_slider_button')
        ActionChains(self.driver).click_and_hold(move_button).perform()
        # for i in range(move_second):
        #     time.perf_counter()
        ActionChains(self.driver).move_by_offset(distance-last_distance, 0).perform()  # perform() 执行,履行
        # 移动最后小于10px 的距离
        self.delay(0.5)
        ActionChains(self.driver).move_by_offset(last_distance, 0).perform()
        self.delay(1)
        # 松开按钮
        ActionChains(self.driver).release().perform()
        self.delay(5)
        if '17716870009' in self.driver.current_url:
            # 点击发送验证码
            self.driver.find_element(By.CLASS_NAME, 'send-code').click()
            iphone_yzm = input('验证码')
            self.driver.find_element(By.XPATH, '//*[@id="sendCode"]/input').send_keys(iphone_yzm)
            self.delay(2)
            self.driver.find_element(By.ID, 'submit').click()
            self.delay(2)
        else:
            # 验证失败,再次验证
            if self.driver.find_element(By.CLASS_NAME, 'geetest_refresh_1').is_displayed():
                self.driver.find_element(By.CLASS_NAME, 'geetest_refresh_1').click()
                self.delay(2)
                self.write_yzm()
            # 判断 点击重试按钮
            elif self.driver.find_element(By.CLASS_NAME, 'geetest_panel_error_content').is_displayed():
                print('提示重试')
                self.driver.find_element(By.CLASS_NAME, 'geetest_panel_error_content').click()
                self.delay(2)
                self.write_yzm()
            elif self.driver.find_element(By.CLASS_NAME, 'jianlian_jianlian_13T').is_displayed():
                cookies = self.driver.get_cookies()
                print(cookies)
                self.save_cookies(cookies)
                print('提示加微信')
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/a/i').click()
                self.delay(4)
        # 登录成功
        print('登录成功')
        cookies = self.driver.get_cookies()
        self.save_cookies(cookies)
        self.driver.find_element(By.ID, 'hqTab').click()
        self.delay(5)


    def process_request(self, request, spider):
        request.cookies = self.cookies
        request.headers.setdefault('User-Agent', self.user_agent)
        return None

    def process_spider_closed(self):
        print('webdriver 关闭')
        self.close_driver()

"""
请求登录的COOKIES:
    cookiesu=641717409901065; 
    device_id=28697ab957c58af6e1bc39514f12cacd; 
s=cj1chgmc9d; 
__utma=1.1253666201.1717411348.1717411348.1717411348.1; 
__utmz=1.1717411348.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 
    Hm_lvt_1db88642e346389874251b5a1eded6e3=1717409902,1717494626,1717501036,1717501108; 
    acw_tc=2760827f17175068951683621e6f021eae8fc06c3f1cb218d2b519746318e1; 
    remember=1; 
    xq_a_token=0060d1c93c77fb305165e3fef50b1526a69b9c7c; 
    xqat=0060d1c93c77fb305165e3fef50b1526a69b9c7c; 
    xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxNzQxMDE0MTQsImlzcyI6InVjIiwiZXhwIjoxNzIwMDAzOTg0LCJjdG0iOjE3MTc1MDY5MDQ3NzYsImNpZCI6ImQ5ZDBuNEFadXAifQ.CiDPYfgNyOdw-nhXcEp7RRhYjPfNh6aRsoUO-q6Clyb1tehjyxmWNcJ9lasliUvIRWHgdOEf6lFUwiQG--cOEZILIZNBpuU3wbjD9nYdYA-RXvWzOzeCs0IjTvIOV1bNFjwM52vg9zA16TXx9Yj5ryZIB4jMM2_MpWEHX6DJApjCGaJa1qTC0vhez1sueRv4pnj_JnD9c5m3s7SLdpWMXP58_fb8ZgkvzZrXAwLkimDVk6ao9VBW1ZWk3vBZbFNDTjTsXT5a40y3FVNd1k6muVIuutQ2R6GBvyaeRnzmzMp4m6Lup51ffx90UZVugsKLrr5oMscGCCD9k_u86j5Reg; 
    xq_r_token=32e36cf3345eb5a1a4a61c66c8358973cd2febf3; 
    xq_is_login=1; 
    u=2174101414; 
    is_overseas=0; 
    .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=mlqiOvxNCUOz4GAKZbl0JiO1fMRxja0R3eZukvv0Di5uPkluDTPwLCBSh6WMl0Q4vfNkgs3iwaBbMbSZ7ECDUw%3D%3D

登录前set-cookie:
首页:
    xq_a_token=c2aefa380b9072a563e961143570e259329d659f
    xqat=c2aefa380b9072a563e961143570e259329d659f
    xq_r_token=2823a23fcab28b5723fbd7c5220a4ba4cc755a52
    xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcxODg0NDcxMiwiY3RtIjoxNzE3NTEyNjk2MDQ3LCJjaWQiOiJkOWQwbjRBWnVwIn0.k_p6xWdWmLxPf9Nz9SVM5fJP1g8iRzVCbkFj_Qo0RwzdCCWel0J4aeDQCF3_uAseGw_eeofbtI1CKXcfNdscrMZYfSGpewFLeCttUV51AOQxsxWlmqcqpKCrVa848N2xZpDV0m1xJGvT-LlQwl87OIPhgb0VaNg7iWPtMTv50OKIyX5BKYtlK3J31-j2WBeqa27QFxXcOvtdXRppxMl06wizxytB9yG6Ly_ApPrHhppoqVw_vCMG5ATz5JxTseDtyjXTijA8CxpoAc9ViJNsU6qX3de48lupcHR1URq-QU731SvUGi4c7jmTtht4SXSaGcvkI79aVd6DnDyga9WG0w
    xq_is_login=
    remember=
    u=641717409901065
https://open.xueqiu.com/mpaas/config/content?keys=security_api_list&cache=false&appkey=92f09797f899bdba4fbf01a2829a16d2
    acw_tc=0bdd344e17175133125362537e93c15c461733210e8a5d91c7a17f18eac79d

点击登录后 set-cookie:
GeeTestAjaxUser=43d0618ee0adefe625d033183bd7c991
"""