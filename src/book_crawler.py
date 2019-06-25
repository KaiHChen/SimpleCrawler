# 通用爬虫，爬取文章，可配置书籍的url,也可以搜索
# BeautifulSoup抓取规则  class = .   id = #  标签直接写

import re

import os
import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
requests.packages.urllib3.disable_warnings()

def download(name, url):
    if url:
        openBook(url, name)
    else:
        url = seachBook(name)
        openBook(url, name)


def seachBook(name):
    print(name)
    return ""


def openBook(url, name):
    config = readConfig(url)
    if config:
        print(config)
        urls = getList(url, config)
        curr = getStartNum(name)
        print(curr)
        print(len(urls))
        for url in urls[curr:len(urls)]:
            url = config['base_url'] + url
            print(url)
            curr = curr + 1
            readContent(url, name, config, curr)
    else:
        print("没有搜索到该网站的配置文件，请到config.json中配置解析信息")


def readContent(url, name, config, curr):
    res = requests.get(url, verify=False, timeout=5, headers=headers)
    res.encoding = config['encoding']
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select(config['title'])
    title = format(title[0].text)
    text = soup.select(config['content'])
    content = format(text[0].text)
    print(title)
    print(content)
    writeText(title, content, name, curr)


def writeText(title, text, name, curr):
    filename = "./books/" + name + ".txt"
    text = re.sub('\s+', '\r\n\t', text).strip('\r\n')
    with open(filename, 'a') as f:
        try:
            f.write(title[int(title.index(".")) + 1:len(title)])
        except ValueError:
            f.write(title)
        f.write("\n")
        f.write(text)
        f.write("\n")
    with open("./books/" + name + ".config", 'w') as f:
        f.write(str(curr) + "\n")
        f.write(title)
    print("已经写完.." + title)


def format(content):
    content = content.replace("章节目录 ", "")
    content = content.replace("show(pc_rd);", "");
    content = content.replace(";show(pc_re);", "")
    content = content.replace("w w w .  . c o m", "")
    try:
        content = content[0:content.index(":var")]
    except ValueError:
        try:
            content = content[0:content.index("var")]
        except ValueError:
            pass
    content = re.sub(u"[.;_()]+", u"", content).strip('\r\n')
    content = content.replace(" ", "")
    content = content.replace("show(pc_rd);", "")
    content = re.sub(u"[a-zA-Z]+", u"", content).strip('\r\n')
    return content


def getList(url, config):
    res = requests.get(url, verify=False, headers=headers, timeout=5)
    soup = BeautifulSoup(res.text, 'html.parser')
    infos = soup.select(config['list'])
    urls = []
    for info in infos:
        url = info.get("href")
        urls.append(url)
    return urls


def getBaseUrl(url):
    reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
    m = re.match(reg, url)
    uri = m.groups()[0] if m else ''
    base_url = uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
    return base_url


def readConfig(url):
    f = open("config.json", encoding='utf-8')
    configs = json.load(f)['config']
    for config in configs:
        baseUrl = getBaseUrl(config['base_url'])
        bookBaseUrl = getBaseUrl(url)
        if bookBaseUrl == baseUrl:
            return config
        else:
            pass


def getStartNum(name):
    config = "./books/" + name + ".config"
    if os.path.exists(config):
        with open(config, 'r') as f:
            sss = f.readline().replace(" ", "")
            print(sss)
            return int(sss)
    else:
        return 0


download("仙帝归来", "https://www.booktxt.com/2_2086/")
