# Scrapy settings for shares_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "shares_scrapy"

SPIDER_MODULES = ["shares_scrapy.spiders"]
NEWSPIDER_MODULE = "shares_scrapy.spiders"


# Obey robots.txt rules 是否遵循robots协议
ROBOTSTXT_OBEY = False

# 系统并发量
CONCURRENT_REQUESTS = 32      # start_requests 一次性会提交32个request给引擎
# 同一网站延迟时间
DOWNLOAD_DELAY = 2
# 自定义随机等待最大时间
RANDOM_DELAY = 4
# 同个域并发量
CONCURRENT_REQUESTS_PER_DOMAIN = 1      # 设置为1 可以理解为顺序进行
# 同IP并发量
CONCURRENT_REQUESTS_PER_IP = 1
# 下载/访问超时时间 超过这个时间就会报Timeout错误
DOWNLOAD_TIMEOUT = 10
# 重试次数
RETRY_TIMES = 1
# 是否启动cookie 引擎
COOKIES_ENABLED = True

# 日志级别  ERROR/WARNING/CRITICAL/DEBUG
LOG_LEVEL = "INFO"
LOG_ENABLED = True
LOG_STDOUT = False   # True 可能会导致scrapyd显示问题

# 关闭spider 的条件
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_ERRORCOUNT = 0


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
              "Safari/537.36")
# 默认请求request headers
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "zh-Hans-CN;q=1",
   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
   "Connection": "keep-alive",
}

# scrapy -redis 配置
# 替换调度器和去重为scrapy-redis
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"              # 调度器
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # scrapy-redis的去重组件
# SCHEDULER_PERSIST = True                                    # 请求URL记录不丢弃, 断点续爬
# # 默认请求队列形式(按优先级)
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"   # 先进先出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"   # 堆栈模式,先进后出

# REDIS_HOST = '192.168.101.103'
# REDIS_PORT = '6379'
# REDIS_PARAMS = {
#    'password': '123456' # redis有密码才设置此项
# }
# 配置持久化
SCHEDULER_FLUSH_ON_START = True  # 是否每次启动清空去重列表
REDIS_START_URLS_BATCH_SIZE = 16 # redis每批次执行request数量



# Enable or disable spider wmiddlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "shares_scrapy.wmiddlewares.SharesScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader wmiddlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# 扩展
EXTENSIONS = {
   "scrapy.extensions.telnet.TelnetConsole": None,
   "shares_scrapy.extensions.ProcessExtension": 300
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "shares_scrapy.pipelines.SharesScrapyPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

HTTPERROR_ALLOWED_CODES = [405, 400]