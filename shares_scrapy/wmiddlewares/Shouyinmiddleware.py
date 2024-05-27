# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Shouyinmiddleware.py
@Author     :wooght
@Date       :2024/5/26 20:10
@Content    :美团收银中间件
"""
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from shares_scrapy.common.SecretCode import Wst
import time
from shares_scrapy.common.w_re import CleanData
from shares_scrapy.wmiddlewares.Webdrivermiddleware import WebdriverMiddleware

class ShouyinMiddleWare(WebdriverMiddleware):
    index_url = 'http://dpurl.cn/TAaQoHkz'
    sy_user = 'wooght'
    sy_password = Wst.decryption('8kkz=YAii=2HV961V8p-7D[-l')
    sy_code = '7370902'
    clearn_data = CleanData('')

    def __init__(self):
        super().__init__(is_proxy=False, maxtime=6, cookie_name='meituan')
        self.headless = False
        self.set_option()

    def set_option(self):
        super().set_option()
        if self.get_url(self.index_url):
            # 先打开网页才能设置cookie
            if len(self.cookies) > 0:
                self.set_cookies(self.cookies)
                self.delay(2)
                # self.driver.refresh()
                self.get_url(self.index_url)
                self.delay(2)
                if '商品' in self.driver.page_source:
                    print('cookie登录成功!')
                    return None
            print('尝试进入iframe进行登录')
            # 进入iframe
            src = self.driver.find_element(By.XPATH, '/html/body/section/iframe').get_attribute('src')
            time.sleep(2)
            # self.driver.switch_to.frame(0)
            self.get_url(src)
            time.sleep(2)
            self.driver.find_element(By.ID, 'part_key').send_keys(self.sy_code)
            self.driver.find_element(By.ID, 'login').send_keys(self.sy_user)
            self.driver.find_element(By.ID, 'password').send_keys(self.sy_password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
            # self.driver.switch_to.parent_frame()
            time.sleep(5)
            self.driver.save_screenshot('common/pic/shouyinresult.png')
            print('登录成功' if '商品' in self.driver.page_source else '登录失败')
            cookies = self.driver.get_cookies()
            self.save_cookies(cookies)
            # self.driver.switch_to.parent_frame()
            # self.new_window()
        else:
            raise IgnoreRequest('访问失败{}'.format(self.index_url))

    def process_request(self, request, spider):
        print('访问spider:{}提供的URL:{}'.format(spider.name, request.url))
        self.get_url(request.url)
        self.delay(1)
        self.set_cookies(self.cookies)
        self.delay(1)
        page = self.get_url(request.url)
        self.delay(1)
        if page:
            self.clearn_data.result_string = self.driver.page_source
            self.clearn_data.delete_html()
            return HtmlResponse(body=self.clearn_data.result_string, encoding='utf-8', request=request, url=request.url)
        else:
            raise IgnoreRequest('访问失败{}'.format(request.url))

"""
    uuid=df692c85f97183d2df89.1716806199.1.0.0;
     _lxsdk_cuid=18fb99fab2ac8-01c31db5f4faf3-6d3b7f53-1bcab9-18fb99fab2ac8;
      _lxsdk=18fb99fab2ac8-01c31db5f4faf3-6d3b7f53-1bcab9-18fb99fab2ac8;
       WEBDFPID=u710124848v65x3913yw59yu8xwxvv0y81uy00uzy3897958360w266x-2032166200612-1716806200028KEKQCEOfd79fef3d01d5e9aadc18ccd4d0c95073221;
        e_u_id_3299326472=c06ac9805ac6ae8c5e1b7b2028c3785b;
         _lxsdk_s=18fb99fab2a-af4-8b1-a20%7C%7C2;
          erp-bsid=hN_hLz4WjGDXH0U4Q6X1N4b-NBgdkohZ_KpYkvr6Q0I8sH1YqizrXXn14XYv6VI4nwTroOGhTyP4GhhKJIqzOA;
           token-for-cors=hN_hLz4WjGDXH0U4Q6X1N4b-NBgdkohZ_KpYkvr6Q0I8sH1YqizrXXn14XYv6VI4nwTroOGhTyP4GhhKJIqzOA;
            retail-poiid=163134577;
             pos_brand=
[{'domain': '.eadtech.cn', 'expiry': 1751366204, 'httpOnly': False, 'name': 'WEBDFPID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '01xuu4092x5150081u0z6952391y36u081uy00uyyvu9795825454838-2032166204847-1716806204302KSQKCSWfd79fef3d01d5e9aadc18ccd4d0c95073584'},
 {'domain': '.retailadmin.eadtech.cn', 'expiry': 1751366204, 'httpOnly': False, 'name': '__mta', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '55336340.1716806204356.1716806204356.1716806204356.1'}, 
 {'domain': '.eadtech.cn', 'expiry': 1716808004, 'httpOnly': False, 'name': '_lxsdk_s', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18fb99fbbb8-601-f19-e89%7C%7CNaN'},
  {'domain': 'retailadmin.eadtech.cn', 'expiry': 1719398204, 'httpOnly': True, 'name': 'erp-bsid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'hN_hLz4WjGDXH0U4Q6X1N4b-NBgdkohZ_KpYkvr6Q0I8sH1YqizrXXn14XYv6VI4nwTroOGhTyP4GhhKJIqzOA'}, 
  {'domain': '.eadtech.cn', 'expiry': 1751366204, 'httpOnly': False, 'name': '_lxsdk', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18fb99fbbb8c8-0b3237111b6541-6d3b7f53-1bcab9-18fb99fbbb8c8'}, 
  {'domain': 'retailadmin.eadtech.cn', 'expiry': 1719398204, 'httpOnly': False, 'name': 'username', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'wooght'}, 
  {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'name', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'WEBDFPID'}, 
  {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'httpOnly', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'False'}, 
  {'domain': '.eadtech.cn', 'expiry': 1751366204, 'httpOnly': False, 'name': '_lxsdk_cuid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18fb99fbbb8c8-0b3237111b6541-6d3b7f53-1bcab9-18fb99fbbb8c8'}, 
  {'domain': 'retailadmin.eadtech.cn', 'expiry': 1719398204, 'httpOnly': False, 'name': 'token-for-cors', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'hN_hLz4WjGDXH0U4Q6X1N4b-NBgdkohZ_KpYkvr6Q0I8sH1YqizrXXn14XYv6VI4nwTroOGhTyP4GhhKJIqzOA'}, 
  {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'path', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '/'}, 
  {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'sameSite', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'Lax'}, 
  {'domain': 'retailadmin.eadtech.cn', 'expiry': 1719398191, 'httpOnly': False, 'name': 'pos_brand', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'MEITUAN'},
   {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'domain', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '.eadtech.cn'},
    {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'expiry', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1751365767'},
     {'domain': 'retailadmin.eadtech.cn', 'expiry': 1719398204, 'httpOnly': False, 'name': 'retail-poiid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '163134577'}, 
     {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'value', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '2472v624797z5u1v01yxww397w5xz2v381uy000897497958746119ux-2032165767657-1716805767101CSWYYIAfd79fef3d01d5e9aadc18ccd4d0c95073324'}, 
     {'domain': 'retailadmin.eadtech.cn', 'httpOnly': False, 'name': 'secure', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'False'}]
"""