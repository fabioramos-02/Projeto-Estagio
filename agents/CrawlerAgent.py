import sqlite3
import requests
from bs4 import BeautifulSoup

class CrawlerAgent:
    def __init__(self):
        # Conecta ao banco de dados
        self.conn = sqlite3.connect('gov_sites.db')

    def get_sites(self):
        """Busca todas as URLs do banco de dados."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT site_name, url FROM sites')
        return cursor.fetchall()

    def crawl(self):
        """Percorre as URLs e processa as imagens."""
        sites = self.get_sites()

        for site_name, url in sites:
            print(f"Processando o site: {site_name} ({url})")
            try:
                response = requests.get(url)
                response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
                soup = BeautifulSoup(response.text, 'html.parser')

                # Buscar imagens sem o atributo alt
                imagens_sem_alt = []
                for img in soup.find_all('img'):
                    if not img.get('alt'):
                        imagens_sem_alt.append(img)

                print(f"Encontradas {len(imagens_sem_alt)} imagens sem texto alternativo em {site_name}")
            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar {url}: {e}")

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
