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

def getContent(url):
    """ 
    获取具体网页的内容
    return:该网页获取到的信息的列表
    """
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
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
            
            return api_text

def getAllAPIContent(inputFile_path):
    """ 
    根据网址列表获取到每个网页的内容
    inputFile_path:网址列表存放的地址
    return:返回获取到的信息的二维列表
    """
    API_list = []
    api_text = []
    api_summary = []
    # 错误处理，事先不知道文件是否存在
    rs = os.path.exists(inputFile_path)
    if rs == True:
        # 打开文件
        fRead = open(inputFile_path,mode = 'r')
        contents = fRead.readlines()
        for name in contents:
            # 去除换行键
            name = name.strip('\n')
            # 保存到现有列表
            API_list.append(name)
    for ConUrl in API_list:
        api_text = getContent('https://www.programmableweb.com'+ConUrl)
        if api_text:
            api_summary.append(api_text)
    return api_summary
    
def listToCsv(list,outputPath):
    """ 
    将二维数组转换成二维表并以csv格式存储在本地
    list:二维数组
    outputPath:输出的文件保存路径
    return:None
    """
    # 定义数据的格式
    columnsName = ['_context','_desc','_about','_headline','_name','_datePublished','_dateModified','_mainEntityOfPage']
    # data里面的数据必须是 2 维列表
    test=pd.DataFrame(columns=columnsName,data=list)
    test.to_csv(outputPath,encoding='gbk')


def main():
    list_url = 'https://www.programmableweb.com/category/all/apis'
    output_fileOfList = 'E://pWebAPIListTest1.txt'
    output_fileOfContent = 'E://pWebAPIContentTest1.csv'
    # getContentURL(list_url,0,3,output_fileOfList)

    apialltest = getAllAPIContent(output_fileOfList)
    listToCsv(apialltest,output_fileOfContent)

main()

