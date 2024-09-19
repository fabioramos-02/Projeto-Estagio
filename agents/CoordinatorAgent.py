import csv
import requests
from agents.CrawlerAgent import CrawlerAgent

class CoordinatorAgent:
    def __init__(self):
        self.crawler = CrawlerAgent()
        self.resultados = []  # Para armazenar os resultados de imagens/divs sem alt

    def run(self):
        # Busca as URLs do banco de dados via CrawlerAgent
        sites = self.crawler.get_sites()

        for site_name, url in sites:
            print(f"Processando o site: {site_name} ({url})")
            try:
                # Faz o rastreamento (crawling) da URL
                response = self.crawler.crawl(url)
                if response is None:
                    print(f"Erro ao acessar o site {url}. Ignorando.")
                    continue

                # Chama a API para analisar o site e encontrar imagens sem alt
                api_url = 'https://sbklpl433e.execute-api.us-east-1.amazonaws.com/teste/analyze'
                payload = {
                    "site_name": site_name,
                    "url": url
                }

                api_response = requests.post(api_url, json=payload)
                if api_response.status_code == 200:
                    # Extraindo o conteúdo de 'body' na resposta da API
                    data = api_response.json().get('body', {})
                    imagens_sem_alt = data.get('imagens_sem_alt', [])

                    if not imagens_sem_alt:
                        print(f"Nenhuma imagem sem 'alt' foi encontrada no site {site_name}.")
                    else:
                        # Armazena os resultados no CSV e para o relatório
                        for img_info in imagens_sem_alt:
                            img_url = img_info['img_url']
                            print(f"Imagem {img_url} encontrada sem texto alternativo.")

                            # Adiciona o resultado à lista
                            self.resultados.append({
                                'site_url': url,
                                'img_url': img_info['img_url'],
                                # 'alt_text_gerado': 'Texto alternativo gerado via API',  # Placeholder
                                'alt_text_original': None,  # Placeholder
                                'tag_completa': img_info['tag_completa']
                            })

                else:
                    print(f"Erro na API para o site {url}: {api_response.status_code}")

            except Exception as e:
                print(f"Erro ao processar o site {url}: {e}")

        # Fechar a conexão do CrawlerAgent
        self.crawler.close()

        # Gera o relatório e salva os resultados em CSV
        if self.resultados:
            print(f"Salvando resultados...")
            self.salvar_resultados_csv()
            self.gerar_relatorio()
        else:
            print("Nenhum resultado para salvar.")

    def gerar_relatorio(self):
        """Gera um relatório simples sobre a quantidade de imagens/divs com/sem alt."""
        total_imagens = len(self.resultados)
        imagens_sem_alt = len(self.resultados)

        print(f"\nRelatório:")
        print(f"Total de imagens/divs processadas: {total_imagens}")
        print(f"Imagens/Divs sem alt: {imagens_sem_alt}")

    def salvar_resultados_csv(self, nome_arquivo='resultados.csv'):
        """Salva os resultados em um arquivo CSV."""
        cabecalho = ['site_url', 'img_url', 'alt_text_gerado', 'alt_text_original', 'tag_completa']

        try:
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=cabecalho)
                writer.writeheader()

                # Escreve cada linha dos resultados no CSV
                for resultado in self.resultados:
                    writer.writerow(resultado)

            print(f"\nResultados salvos em {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo CSV: {e}")
