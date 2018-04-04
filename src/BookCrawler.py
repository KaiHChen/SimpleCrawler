# 抓取顶点小说和笔趣乐内容，直接搜索名字开始下载，没有使用多线程，没有断点！！！

import re
import requests
from bs4 import BeautifulSoup

search_url_start = "http://zhannei.baidu.com/cse/search?q="

# 顶点小说
search_url_end_dd = "&click=1&s=1682272515249779940&nsid="
# 笔趣乐
search_url_end_bq = "&s=2413017012796817192&entry=1"

# type 使用搜索地址 1 顶点小说  2 笔趣乐
def search(book, type):
    info = getBookInfoUrl(book, type)
    if info:
        url = info.get("href")
        print(url)
        filename = book + ".txt"
        if type == 1:
            urls = getSection(url)
        elif type == 2:
            urls = getSectionBQ(url)
        print(urls)
        for uu in urls:
            contenturl = url + uu + ".html"
            print(contenturl)
            if type == 1:
                readText(contenturl, filename)
            elif type == 2:
                readTextBQ(contenturl, filename)
    else:
        print("没有搜到" + book)


def getBookInfoUrl(book, type):
    url = search_url_start + book
    if type == 1:
        url = url + search_url_end_dd
    elif type == 2:
        url = url + search_url_end_bq
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    infos = soup.select('.result-game-item-detail h3 a')
    for info in infos:
        if info.get("title") == book:
            return info
    return


def getSection(url):
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    infos = soup.select('.chapterlist dd a')
    urls = []
    for info in infos:
        info.text
        url = info.get("href")
        urls.append(url[0:len(url) - 5])
    urls = list(set(urls))
    list.sort(urls)
    return urls


def getSectionBQ(url):
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    infos = soup.select('.article-list dd a')
    urls = []
    for info in infos:
        info.text
        url = info.get("href")
        urls.append(url[0:len(url) - 5])
    return urls


def readText(url, filename):
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('.inner h1')
    print(title[0].text)
    text = soup.select('.inner #content')
    print(text[0].text)
    writeText(title[0].text.replace("_", "") + '\n', text[0].text + '\n', filename)


def readTextBQ(url, filename):
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    title = soup.select('.bookname h1')
    title_text = title[0].text.replace("正文 ", "")
    print(title_text)
    text = soup.select('.content_read #content')
    content = text[0].text.replace(" 一秒记住【笔÷趣♂乐 WwW.BiquLe.Com】，精彩小说无弹窗免费阅读！", "")
    print(content)
    writeText(title_text + '\n', content + '\n', filename)


def writeText(title, text, filename):
    section_text = re.sub('\s+', '\r\n\t', text).strip('\r\n')
    with open(filename, 'a') as f:
        f.write(title)
        f.write(section_text)
    print("已经写完.." + title)


search("校园绝品狂神", 2)
