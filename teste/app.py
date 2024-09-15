import requests
from bs4 import BeautifulSoup
import logging

import os

# Configura o logging
logging.basicConfig(filename='imagem_report.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def baixar_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Falha ao baixar a página {url}: {e}")
        return None


def analisar_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    imagens = soup.find_all('img')
    imagens_sem_alt = []

    for i, img in enumerate(imagens):
        alt_text = img.get('alt')
        if alt_text:
            logging.info(f"Imagem {i + 1}: possui texto alternativo '{alt_text}'")
        else:
            logging.warning(f"Imagem {i + 1}: NÃO possui texto alternativo")
            imagens_sem_alt.append(img)

    return imagens_sem_alt


def sugerir_texto_alternativo(imagem):
    # Aqui você deve implementar a lógica de sugestão usando IA.
    # Para simplificação, estamos retornando um texto padrão.
    return "Texto alternativo sugerido pela IA"


def corrigir_imagens_sem_alt(imagens_sem_alt):
    for i, img in enumerate(imagens_sem_alt):
        sugestao = sugerir_texto_alternativo(img)
        logging.info(f"Imagem {i + 1}: sugerido texto alternativo '{sugestao}'")


def processar_url(url):
    html = baixar_html(url)
    if html:
        imagens_sem_alt = analisar_html(html)
        if imagens_sem_alt:
            corrigir_imagens_sem_alt(imagens_sem_alt)
        else:
            logging.info("Todas as imagens possuem texto alternativo.")
    else:
        logging.error("Não foi possível realizar a análise da página.")


def main(urls):
    for url in urls:
        logging.info(f"Processando URL: {url}")
        processar_url(url)


if __name__ == "__main__":
    urls = ["https://www.ms.gov.br/", "https://bioparquepantanal.ms.gov.br/"]
    main(urls)
