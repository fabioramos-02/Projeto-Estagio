
from agents.CrawlerAgent import CrawlerAgent

if __name__ == "__main__":
    crawler = CrawlerAgent()
    crawler.crawl()
    crawler.close()