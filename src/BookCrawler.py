# 抓取顶点小说内容，直接搜索名字开始下载，没有使用多线程，没有断点！！！

import re
import requests
from bs4 import BeautifulSoup

search_url_start = "http://zhannei.baidu.com/cse/search?q="
search_url_end = "&click=1&s=1682272515249779940&nsid="


def search(book):
    info = getBookInfoUrl(book)
    if info:
        url = info.get("href")
        print(url)
        filename = book + ".txt"
        urls = getSection(url)
        for uu in urls:
            contenturl = url + uu + ".html"
            print(contenturl)
            readText(contenturl, filename)
    else:
        print("没有搜到" + book)


def getBookInfoUrl(book):
    url = search_url_start + book + search_url_end
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


def readText(url, filename):
    res = requests.get(url, )
    print(res.url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('.inner h1')
    print(title)
    text = soup.select('.inner #content')
    print(text[0].text)
    writeText(title[0].text + '\n', text[0].text + '\n', filename)


def writeText(title, text, filename):
    title_text = re.sub('\s+', '\r\n\t', title).strip('\r\n')
    section_text = re.sub('\s+', '\r\n\t', text).strip('\r\n')
    with open(filename, 'a') as f:
        f.write(title_text)
        f.write(section_text)
    print("已经写完.." + title_text)


search("太古魔仙")
