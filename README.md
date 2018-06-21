# SimpleCrawler
简单的python爬虫

## book_crawler.py
	小说爬虫，需要配置config.json文件
	{
    "config": [
        {
            "base_url": "https://www.bqg5200.com", //base地址，搜索目录后，需要添加到目录签名
            "search_url": "", //搜索地址
            "list": "#readerlist li a", //目录搜索规则
            "title": ".title h1", //标题过滤规则
            "content": "#content", //内容过滤规则
            "encoding": "gbk" //网页格式
        }
      ]
	}
	
	

