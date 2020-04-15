# pWebCrawler
crawl programmableweb data

- ##### `pWebAPIContentTest1.csv`

  - 输出数据示例

- ##### `pWebAPIListTest1.txt`

  - 内容详情页网址列表

- ##### `CrawlerAPIList.py` 

  - 获取内容详情页网址列表
  - 使用 selenium 下载网页

- ##### `CrawlerAPITest.py`

  - 测试文件

- ##### `CrawlerAPIContent.py` 

  - 根据网址列表爬取具体内容
  - 使用 request 获取网页
  - 使用 bs4 库和 re 库解析网页

- ##### `pWebSpider` 

  - 功能类似 CrawlerAPIContent.py，性能提升两倍
  - 使用 scrapy 框架