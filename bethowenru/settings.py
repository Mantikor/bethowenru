# Scrapy settings for bethowenru project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "bethowenru"

SPIDER_MODULES = ["bethowenru.spiders"]
NEWSPIDER_MODULE = "bethowenru.spiders"

API_BASE_URL = 'https://www.bethowen.ru/***/******/****/v*'

EP_START = '{}/*****/*****/********'.format(API_BASE_URL)
EP_AUTH = '{}/*****/*****/********'.format(API_BASE_URL)
EP_FEED_CATEGORIES = '{}/*****/*****/**********'.format(API_BASE_URL)
EP_PROD_CATEGORIES = '{}/*********/**********'.format(API_BASE_URL)
EP_CATEGORY_ITEMS = '{}/*********/****'.format(API_BASE_URL) + '?category_id={}&sort_type=popular&offset={}&limit={}'
EP_ITEM_INFO = '{}/*********/*******'.format(API_BASE_URL) + '?product_id={}'
EP_LIST_CITIES = '{}/*******/******'.format(API_BASE_URL) + '?city_type=with_shop'

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': '***************************************************',
    'X-***************': '247',
    'X-**********': '84',
    'X-************': '************************************',
    'Host': 'www.bethowen.ru',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

AUTH_DATA = {
    'login': '*************',
    'password': '********'
}

PROXY_LIST = [{'user': '***', 'password': '*****', 'ip': '192.168.88.11'}, {'user': '*****', 'password': '****', 'ip': '192.168.88.12'},
              {'user': '****', 'password': '****', 'ip': '192.168.88.13'}, {'user': '****', 'password': '****', 'ip': '192.168.88.14'}]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "bethowenru (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "bethowenru.middlewares.BethowenruSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "bethowenru.middlewares.BethowenruSetProxyMiddleware": 200,
   # "bethowenru.middlewares.BethowenruDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "bethowenru.pipelines.BethowenruPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
