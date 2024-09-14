from agents.AltTextGeneratorAgent import AltTextGeneratorAgent
from agents.AnalyzerAgent import AnalyzerAgent
from agents.CrawlerAgent import CrawlerAgent

class CoordinatorAgent:
    def __init__(self):
        self.crawler = CrawlerAgent()
        self.analyzer = AnalyzerAgent()
        self.alt_text_generator = AltTextGeneratorAgent()

    def run(self):
        # Busca as URLs do banco de dados via CrawlerAgent
        sites = self.crawler.get_sites()

        for site_name, url in sites:
            print(f"Processando o site: {site_name} ({url})")
            try:
                # Faz o rastreamento (crawling) da URL e obtém o HTML
                response = self.crawler.crawl(url)
                if response is None:
                    continue

                html = response.text

                # Analisa o HTML em busca de imagens sem alt e gera texto alternativo
                imagens_sem_alt = self.analyzer.analyze(html, url) # Lista de imagens sem alt

                for img_info in imagens_sem_alt:
                    img_url = img_info['img_url']
                    alt_text = img_info['alt_text']
                    print(f"Imagem {img_url}: texto alternativo sugerido '{alt_text}'")
            
            except Exception as e:
                print(f"Erro ao processar o site {url}: {e}")

        # Fechar a conexão do CrawlerAgent
        self.crawler.close()
