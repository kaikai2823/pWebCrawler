import requests
from bs4 import BeautifulSoup
import bs4
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def startSeleniumGetHTML(url):
    """ 
    使用 selenium 来获取网页
    url:目标网址
    return:网页源代码
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 解决报错 handshake failed; returned -1, SSL error code 1, net_error -100
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')  ##忽略https错误
        chrome_options.add_argument('--load-images=no')  ##关闭图片加载
        chrome_options.add_argument('--disk-cache=yes')  ##开启缓存
        # executable_path 是 Chromedriver 的执行路径
        chrome = webdriver.Chrome(executable_path="E:/Tools/chromedriver_win32/chromedriver.exe",chrome_options=chrome_options)
        chrome.get(url)
        return chrome.page_source
    except:
        return ""

def getContentURL(url,preNum,endNum,fpath):
    """ 
    解析网页获取 api 列表网址的标记信息
    url:目标网站的网址头部
    preNum:爬取网页的起始号码
    endNum:爬取网页的结束号码
    fpath:获取的内容存放地址
    return:None
    """
    count = 0
    for i in range(preNum,endNum):
        cata_url = url + '?page=' + str(i)
        try:
            html = startSeleniumGetHTML(cata_url)
            soup = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
            for td in soup.find_all('td','views-field views-field-pw-version-title'):
                if isinstance(td,bs4.element.Tag):
                    with open(fpath,'a',encoding="utf-8") as f:
                        f.write(str(td.find('a').get('href'))+'\n')
            count = count + 1
            print("\r当前进度:{:.2f}%".format(count*100/(endNum-preNum)))
        except:
            print("第{:d}页获取失败！".format(i))
            count = count + 1
            print("\r当前进度:{:.2f}%".format(count*100/(endNum-preNum)))
            continue

def main():
    url = 'https://www.programmableweb.com/category/all/apis'
    output_file = 'E://pWebAPIList.txt'
    getContentURL(url,2000,2103,output_file)

main()