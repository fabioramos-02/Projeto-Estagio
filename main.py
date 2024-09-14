from agents.AltTextGeneratorAgent import AltTextGeneratorAgent
from agents.AnalyzerAgent import AnalyzerAgent
from agents.CrawlerAgent import CrawlerAgent
from agents.CoordinatorAgent import CoordinatorAgent

if __name__ == "__main__":
    crawler = CrawlerAgent()
    crawler.crawl()
    crawler.close()