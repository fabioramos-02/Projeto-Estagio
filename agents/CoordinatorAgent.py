import csv
from agents.AltTextGeneratorAgent import AltTextGeneratorAgent
from agents.AnalyzerAgent import AnalyzerAgent
from agents.CrawlerAgent import CrawlerAgent

class CoordinatorAgent:
    def __init__(self):
        self.crawler = CrawlerAgent()
        self.analyzer = AnalyzerAgent()
        self.alt_text_generator = AltTextGeneratorAgent()
        self.resultados = []  # Para armazenar os resultados de imagens/divs sem alt

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

                # Analisa o HTML em busca de imagens e divs com background-image
                imagens_sem_alt = self.analyzer.analyze(html, url)
                divs_sem_alt = self.analyzer.analyze_background_images(html, url)

                # Mescla os resultados das imagens e das divs
                todas_imagens_sem_alt = imagens_sem_alt + divs_sem_alt

                for img_info in todas_imagens_sem_alt:
                    img_url = img_info['img_url']
                    alt_text = img_info['alt_text_gerado']
                    print(f"Imagem {img_url}: texto alternativo sugerido '{alt_text}'")

                    # Armazena os resultados para o CSV e relatório
                    self.resultados.append({
                        'site_url': img_info['site_url'],
                        'img_url': img_info['img_url'],
                        'alt_text_gerado': img_info['alt_text_gerado'],
                        'alt_text_original': img_info['alt_text_original'],
                        'tag_completa': img_info['tag_completa']
                    })

            except Exception as e:
                print(f"Erro ao processar o site {url}: {e}")

        # Fechar a conexão do CrawlerAgent
        self.crawler.close()

        # Gera o relatório e salva os resultados em CSV
        self.gerar_relatorio()
        self.salvar_resultados_csv()

    def gerar_relatorio(self):
        """Gera um relatório simples sobre a quantidade de imagens/divs com/sem alt."""
        total_imagens = len(self.resultados)
        imagens_sem_alt = len([img for img in self.resultados if not img['alt_text_original']])
        imagens_com_alt = total_imagens - imagens_sem_alt

        print(f"\nRelatório:")
        print(f"Total de imagens/divs processadas: {total_imagens}")
        print(f"Imagens/Divs sem alt: {imagens_sem_alt}")
        print(f"Imagens/Divs com alt: {imagens_com_alt}")

    def salvar_resultados_csv(self, nome_arquivo='resultados.csv'):
        """Salva os resultados em um arquivo CSV."""
        cabecalho = ['site_url', 'img_url', 'alt_text_gerado', 'alt_text_original', 'tag_completa']

        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=cabecalho)
            writer.writeheader()

            # Escreve cada linha dos resultados no CSV
            for resultado in self.resultados:
                writer.writerow(resultado)

        print(f"\nResultados salvos em {nome_arquivo}")
