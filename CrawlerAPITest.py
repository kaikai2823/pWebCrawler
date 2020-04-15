import requests
from bs4 import BeautifulSoup
import bs4
import re
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def getHTMLText(url):
    try:
        r = requests.get(url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
             },timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getHTMLTextUseUrlLib(url):
    try:
        r = urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
        re = urllib.request.urlopen(r)
        return re.read()
    except:
        return ""

def startSeleniumGetHTML(url):
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

        chrome = webdriver.Chrome(executable_path="E:/Tools/chromedriver_win32/chromedriver.exe",chrome_options=chrome_options)
        chrome.get(url)
        return chrome.page_source
    except:
        return ""

def getContentURL(url,preNum,endNum,fpath):
    count = 0
    for i in range(preNum,endNum):
        cata_url = url + '?page=' + str(i)
        try:
            # html = getHTMLText(cata_url)
            html = startSeleniumGetHTML(cata_url)
            # html = getHTMLTextUseUrlLib(cata_url)
            soup = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
            # for tr in soup.find('tbody').children:
            #     if isinstance(tr,bs4.element.Tag):
            #         tds = tr('td')
            #         cList.append([tds[0].string, tds[1].string, tds[2].string])
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
def getContent(url,fpath):
    """ 
    获取具体网页的内容
    """
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
    api_summary = []
    for sc in soup.find_all('script',type="application/ld+json"):
        if isinstance(sc,bs4.element.Tag):
            api_text = []
            content = sc.string
            _context = re.findall(r'\"@context\": \".*?\"',content)
            _desc = re.findall(r'\"description\": \".*?\"',content)
            _about = re.findall(r'\"about\": \[[\s\S]*?\]',content)
            _headline = re.findall(r'\"headline\": \".*?\"',content)
            _name = re.findall(r'\"name\": \".*?\"',content) # 有多个匹配
            _datePublished = re.findall(r'\"datePublished\": \".*?\"',content)
            _dateModified = re.findall(r'\"dateModified\": \".*?\"',content)
            _mainEntityOfPage = re.findall(r'\"mainEntityOfPage\": \".*?\"',content)
            
            api_text.append(_context[0].split(":",1)[1])
            api_text.append(_desc[0].split(":",1)[1])
            api_text.append(_about[0].split(":",1)[1])
            api_text.append(_headline[0].split(":",1)[1])
            api_text.append(_name[0].split(":",1)[1])
            api_text.append(_datePublished[0].split(":",1)[1])
            api_text.append(_dateModified[0].split(":",1)[1])
            api_text.append(_mainEntityOfPage[0].split(":",1)[1])
            
            api_summary.append(api_text)
    columnsName = ['_context','_desc','_about','_headline','_name','_datePublished','_dateModified','_mainEntityOfPage']
    # data里面的数据必须是 2 维列表
    test=pd.DataFrame(columns=columnsName,data=api_summary)
    print(test)
            
def main():
    url = 'https://www.programmableweb.com/category/all/apis'
    output_fileOfList = 'E://pWebAPIListTest1.txt'
    output_fileOfContent = 'E://pWebAPIContentTest1.txt'
    # getContentURL(url,0,3,output_fileOfList)
    # API_list = []
    # # 错误处理，事先不知道文件是否存在
    # rs = os.path.exists(output_fileOfList)
    # if rs == True:
    #     # 打开文件
    #     fRead = open(output_fileOfList,mode = 'r')
    #     contents = fRead.readlines()
    #     for name in contents:
    #         # 去除换行键
    #         name = name.strip('\n')
    #         # 保存到现有列表
    #         API_list.append(name)
    # for ConUrl in API_list:
    getContent('https://www.programmableweb.com'+'/api/google-earth',output_fileOfContent)

main()

