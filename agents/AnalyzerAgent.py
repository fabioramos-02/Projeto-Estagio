from autogen import Agent
from bs4 import BeautifulSoup

class AnalyzerAgent(Agent):
    def __init__(self):
        super().__init__()

    def analyze(self, html):
        # Implementação do método analyze
        soup = BeautifulSoup(html, 'html.parser')
        imagens_sem_alt = []
        for img in soup.find_all('img'):
            if not img.get('alt'):
                imagens_sem_alt.append(img)
        return imagens_sem_alt
