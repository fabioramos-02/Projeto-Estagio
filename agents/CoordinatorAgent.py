from autogen import Agent
import requests

from agents.AltTextGeneratorAgent import AltTextGeneratorAgent
from agents.AnalyzerAgent import AnalyzerAgent
from agents.CrawlerAgent import CrawlerAgent
class CoordinatorAgent(Agent):
    def __init__(self):
        super().__init__()
        self.crawler = CrawlerAgent()
        self.analyzer = AnalyzerAgent()
        self.alt_text_generator = AltTextGeneratorAgent()

    def run(self, start_url):
        # Fluxo principal do programa
        html = requests.get(start_url).text
        imagens_sem_alt = self.analyzer.analyze(html)
        for img in imagens_sem_alt:
            img_url = img['src']
            alt_text = self.alt_text_generator.generate_alt_text(img_url)
            print(f"Imagem {img_url}: texto alternativo sugerido '{alt_text}'")
