import requests
from bs4 import BeautifulSoup

def baixar_html(url):
    # Faz uma requisição HTTP para a URL
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        return response.text
    else:
        print(f"Falha ao baixar a página: {response.status_code}")
        return None

def analisar_html(html):
    # Analisa o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Encontra todas as tags <img> no HTML
    imagens = soup.find_all('img')
    
    # Extrai as informações de cada imagem
    for i, img in enumerate(imagens):
        alt_text = img.get('alt')
        if alt_text:
            print(f"Imagem {i + 1}: possui texto alternativo '{alt_text}'")
        else:
            print(f"Imagem {i + 1}: NÃO possui texto alternativo")

# URL alvo
url = "https://exemplo.gov.br"

# Baixa o HTML da página
html = baixar_html(url)

# Se o HTML foi baixado com sucesso, realiza a análise
if html:
    analisar_html(html)
