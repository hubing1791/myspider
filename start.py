from scrapy.cmdline import execute
import sys


class StartCrawl:
    def __init__(self):
        pass

    @staticmethod
    def start(spider_name: str):
        # print(spider_name)
        execute(['scrapy', 'crawl', spider_name])


if __name__ == '__main__':
    StartCrawl.start(sys.argv[1])
