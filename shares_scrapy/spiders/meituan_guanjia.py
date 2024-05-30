import time
from typing import Iterable

import scrapy
from scrapy import Request, FormRequest
from scrapy.utils.project import get_project_settings
import json
import chardet

class MeituanGuanjiaSpider(scrapy.Spider):
    default_headers = get_project_settings().get('DEFAULT_REQUEST_HEADERS')
    name = "meituan_guanjia"
    raw_json = '[{"ch":"AppStore","msid":"CFFD1744-092C-444C-AAC4-057FF12CB4981717061597359835","lch":"erp_retail_admin","bht":"off","app":"1.18.10","localId":"19b182cb45b04500d3a9cd872910ce9691eaec6f38436be23d","uuid":"0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387","category":"data_sdk_eco","evs":[{"val_bid":"b_6ciybp5j","lx_inner_data":{"seq":12,"rtm":1717061867626,"net_retry":0,"net_time":48},"req_id":"8858637A-1739-4E23-832A-F305B3E15EB7","refer_req_id":"AAAAD9C8-E475-44BC-B629-63B85A61E253","val_ref":"CMTLoginPageVC","nm":"MC","stm":1717061866240,"seq":12,"tm":1717061866240,"val_cid":"c_zh5uep1k","val_lab":{},"isauto":7,"nt":1}],"subcid":"MEITUAN","union_id":"183f2b1959f4472b92bf813928b4498ba164619479778148387","ct":"iphone","buildid":"1131","sdk_ver":"4.15.6","os":"17.4.1","net":"WIFI","appnm":"erp_retail_admin","mac":"020000000000","mno":"--","pushid":"0","cnfver":"-1","idfv":"DEF354A1-18E7-4BCC-A2B4-9A43AE940BD2","ps":0,"sc":"1170*2532","dm":"iPhone 12","idfa":"00000000-0000-0000-0000-000000000000"},{"ch":"AppStore","msid":"CFFD1744-092C-444C-AAC4-057FF12CB4981717061597359835","lch":"erp_retail_admin","bht":"off","app":"1.18.10","localId":"19b182cb45b04500d3a9cd872910ce9691eaec6f38436be23d","uuid":"0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387","category":"data_sdk_eco","evs":[{"val_bid":"b_s0bt64z7","lx_inner_data":{"rtm":1717061867626,"seq":13},"req_id":"8858637A-1739-4E23-832A-F305B3E15EB7","refer_req_id":"AAAAD9C8-E475-44BC-B629-63B85A61E253","val_ref":"CMTLoginPageVC","nm":"SC","stm":1717061867058,"seq":13,"tm":1717061867058,"val_cid":"c_890jzhpj","val_lab":{"tenant_id":"7370902"},"isauto":7,"nt":1},{"lx_inner_data":{"rtm":1717061867626,"seq":14},"req_id":"8858637A-1739-4E23-832A-F305B3E15EB7","refer_req_id":"AAAAD9C8-E475-44BC-B629-63B85A61E253","val_ref":"CMTLoginPageVC","nm":"PD","stm":1717061867080,"seq":14,"tm":1717061867080,"val_lab":{"duration":"12162"},"val_cid":"CMTLoginPageVC","nt":1,"isauto":6},{"lx_inner_data":{"rtm":1717061867626,"seq":15},"req_id":"648F2ADA-78FF-46F9-B26D-8C5DFBFEC9F2","refer_req_id":"8858637A-1739-4E23-832A-F305B3E15EB7","val_ref":"CMTLoginPageVC","nm":"PV","stm":1717061867087,"seq":15,"tm":1717061867087,"val_lab":{"custom":{"_phpage":"Retail.LoadingViewController"}},"val_cid":"Retail.LoadingViewController","nt":1,"isauto":6}],"subcid":"MEITUAN","union_id":"183f2b1959f4472b92bf813928b4498ba164619479778148387","ct":"iphone","buildid":"1131","sdk_ver":"4.15.6","os":"17.4.1","net":"WIFI","appnm":"erp_retail_admin","mac":"020000000000","mno":"--","pushid":"0","idfv":"DEF354A1-18E7-4BCC-A2B4-9A43AE940BD2","ps":0,"sc":"1170*2532","dm":"iPhone 12","idfa":"00000000-0000-0000-0000-000000000000"}]'
    ios_update_json = json.loads(raw_json)
    start_urls = [
        "https://catdot.dianping.com/broker-service/api/config?op=all&v=3&appId=139&appVersion=11810&compress=true",
        "https://catdot.dianping.com/broker-service/commandbatch?r={}&v=8&p=139&unionId=00000000-0000-0000-0000-000000000000"
    ]

    def start_requests(self) -> Iterable[Request]:
        print('组装request...')
        headers = {}
        for key,value in self.default_headers.items():
            headers[key] = value
        headers['User-Agent'] = "Mozilla/5.0 (iPhone unknown) AppleWebKit/unknown (KHTML, like Gecko) Mobile/unknown TitansX/11.40.0 KNB/1.0 iOS/17.4.1 meituangroup/com.meituan.erp.retail.admin/1.18.10 meituangroup/1.18.10 App/(null)/1.18.10 iPhone/iPhone12 WKWebView"
        # headers['deviceModel'] = "iPhone13,2"
        # headers['deviceBrand'] = "iPhone"
        # headers['appVersion'] = "11810"
        # headers['platform'] = "iOS"
        # headers['platVersion'] = "17.4.1"
        headers['HOST'] = "retailadmin-erp.meituan.com"
        # headers['Content-Type'] = "application/json;charset=UTF-8"
        headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        headers['Accept-Language'] = "zh-CN,zh-Hans;q=0.9"
        # headers['Content-Length'] = "749"
        print(len(self.raw_json))
        print(headers)
        transport_json = {}
        for key, value in self.ios_update_json[0].items():
            print(key, value)
            if isinstance(value, dict):
                transport_json[key] = {}
                for k, v in value.items():
                    transport_json[key][k] = str(v)
            else:
                transport_json[key] = str(value)
        # yield FormRequest(url=self.start_urls[1], json=transport_json,
        #                   callback=self.parse, method="PUT", errback=self.parse_err, headers=headers)
        current_url = self.start_urls[1].format(str(int(time.time()*1000)))
        print(current_url)
        raw_cookies = '_utm_content=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387; cityid=0; dpid=; network=wifi; uuid=0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387'.split(';')
        cookies = {}
        for cookie in raw_cookies:
            temp = cookie.split('=')
            cookies[temp[0].strip()] = temp[1].strip()
        for key, value in cookies.items():
            print(key, value)
        current_url = 'https://retailadmin-erp.meituan.com/commodity.html?bizlogintoken=0yMpWXundnvIY1gasvxUw33O-zeju9HRo8X6Vsdq_DI8pOHR63RbZDMFZJfGUThVauAHaMJnvAqDc7LmCYdpjg&poiId=163134577&version=1.1.0&native_version=1.18.10&webview_launch=1717061867916&pos_brand=MEITUAN&bottombar_height=147.0'
        yield Request(url=current_url, method='GET', headers=headers, cookies=cookies)

    def parse(self, response, *args):
        print('成功到parse')
        for key, value in response.request.headers.items():
            print(key, value)
        print("返回结果:")
        result_body = response.body
        print(result_body)
        print("返回headers")
        print(response.headers)
        print(response.request.body)

    def parse_err(self, failure):
        print('错误:...')
        print(failure.__class__.__name__)
        print(failure.value)


"""
登录前:
https://api-unionid.meituan.com/unionid/ios/update
    传递json:
        {"appInfo":{"app":"com.meituan.erp.retail.admin","version":"1.18.10","sdkVersion":"1.7.8"},"communicationInfo":{"nop":"--"},"environmentInfo":{"osVersion":"17.4.1","osName":"iOS","clientType":"iphone","platform":"iOS"},"deviceInfo":{"secondaryDeviceInfo":{"signature":"d441f2bc79adf3cb3f55c4ebda30901a"},"deviceModel":"iPhone 12","keyDeviceInfo":{"idfa":"00000000-0000-0000-0000-000000000000","idfv":"87B522E9-EAD2-4982-BD0B-AE05689FF484"},"isJailBreak":false},"idInfo":{"uuid":"0000000000000183F2B1959F4472B92BF813928B4498BA164619479778148387","requiredId":1,"dpid":"183f2b1959f4472b92bf813928b4498ba164619479778148387","localId":"19b182cb45b04500d3a9cd872910ce9691eaec6f38436be23d","unionId":"183f2b1959f4472b92bf813928b4498ba164619479778148387"}}
    返回json:
        {"code":0,"message":null,"data":{"unionId":"183f2b1959f4472b92bf813928b4498ba164619479778148387"},"serviceStatus":0}

https://catdot.dianping.com/broker-service/api/config?op=all&v=3&appId=139&appVersion=11810&compress=true

https://appsec-mobile.meituan.com/v5/sign
"""