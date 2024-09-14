import sqlite3
import requests

class CrawlerAgent:
    def __init__(self):
        # Conecta ao banco de dados
        self.conn = sqlite3.connect('db/gov_sites.db')

    def get_sites(self):
        """Busca todas as URLs do banco de dados."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT site_name, url FROM sites')
        return cursor.fetchall()

    def crawl(self, url):
        """Faz a requisição HTTP e retorna o conteúdo HTML."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
