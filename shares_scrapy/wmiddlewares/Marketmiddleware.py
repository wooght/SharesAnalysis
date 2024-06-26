# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Marketmiddleware.py
@Author     :wooght
@Date       :2024/4/29 15:16
@Content    :行情下载中间件
"""
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time, sys, json, random
from shares_scrapy.common.echo import echo
from shares_scrapy.common.w_re import CleanData
from shares_scrapy.run.GetProxy import GetProxy

class Marketmiddleware(object):
    proxy_ip = GetProxy('proxy_ips')

    def __init__(self):
        self.options = Options()
        self.headless = True  # 无头模式
        self.url = ''  # 访问地址
        self.body = ''  # response 返回内容
        self.webdriver = webdriver
        self.handles = []
        self.total_crawl = 0
        self.get_ip_nums = 0
        self.current_ip = ''
        self.ip_status = True
        self.set_options()


    def set_options(self):
        """
        启动webdriver
        content:
            设置options
            设置代理ip
            启动webdirver并打开默认网页供后续运行JS用
        :return:
        """
        current_ip = self.proxy_ip.get_ip()                             # 获取IP,每启动一次webdriver 就获取一次IP
        self.current_ip = current_ip if current_ip else sys.exit()      # 如果获取不到代理,退出系统
        if self.headless:
            # 开启无头模式
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1600,900")  # 窗口大小
        self.options.add_argument("lang=zh_CN.UTF-8")   # 编码
        self.options.add_argument("--no-sandbox")  # 沙盒模式
        self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        self.options.add_argument('log-level=3')    # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
        }
        self.options.add_experimental_option('prefs', prefs)
        proxy_str = '--proxy-server=http://{}'.format(self.current_ip)
        self.options.add_argument(proxy_str)         # 设置代理IP
        print('设置成功!'+str(proxy_str))

        self.driver = self.webdriver.Chrome(options=self.options)  # 启动chromedriver
        self.driver.set_page_load_timeout(10)       # 设置timeout最大时间
        page = self.get_url('https://finance.sina.com.cn/realstock/company/sz002594/nc.shtml')
        if not page:
            self.close_driver()
        elif len(self.driver.page_source) < 100:
            print('获取内容失败!{}'.format(self.driver.page_source))
            self.close_driver()
        else:
            self.handles.append(self.driver.current_window_handle)
            self.driver.implicitly_wait(3)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/a[3]').click()
            self.handles.append(self.driver.current_window_handle)

    def close_driver(self):
        """
        重启webdriver 入口
        :return:
        """
        self.driver.close()
        self.driver.quit()
        self.set_options()

    def process_request(self, request, spider):
        """
        webdriver 执行爬取操作
        content:    随机暂停
                    切换handle
                    获取内容或者触发异常
                    获取JS返回内容
        :param request:
        :param spider:
        :return: IgnoreRequest HtmlResponse
        """
        self.total_crawl += 1
        # 第二个handle获取数据
        time.sleep(random.randint(2, 4))
        if self.total_crawl % 10 == 0:
            print('downloadmiddleware 每10次停留2分钟')
            time.sleep(5)
        print('downloadmiddleware  download->'+request.url)
        self.driver.switch_to.window(self.driver.window_handles[1])             # 切换到最后一个handle
        page = self.get_url(request.url)
        if not page:
            self.close_driver()
            raise IgnoreRequest('打开连接失败,proxy ip :{}'.format(self.current_ip))
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
        print('downloadmiddleware download 成功')
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


    def get_url(self, url):
        print('proxyip{}尝试打开地址:{}'.format(self.current_ip, url))
        try:
            self.driver.get(url)
            # WebDriverWait(self.driver, 10).until(presence_of_element_located((By.XPATH, '/html/head/title')))
            # print(self.driver.execute_script("return {httpStatus: document.httpStatus, status: document.status};"))
            return True
        except Exception as e:
            print(f'.....错误{type(e).__name__}....')
            print(e)
            return False


"""
    WebDriverException :Message: unknown error: net::ERR_TUNNEL_CONNECTION_FAILED
    TimeoutException
    NoAlertPresentException
"""