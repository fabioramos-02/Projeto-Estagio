import json
import requests
from bs4 import BeautifulSoup

def analyze_images(html, site_url):
    soup = BeautifulSoup(html, 'html.parser')
    imagens_sem_alt = []

    for img in soup.find_all('img'):
        alt_text = img.get('alt')
        img_url = img.get('src')

        if not alt_text or alt_text.strip() == "":
            imagens_sem_alt.append({
                'img_url': img_url,
                'tag_completa': str(img)
            })

    return imagens_sem_alt

def lambda_handler(event, context):
    try:
        # Checar se os parâmetros estão no evento diretamente
        url = event.get('url', 'http://www.acadepol.ms.gov.br')  # Valor padrão
        site_name = event.get('site_name', 'ACADEPOL')  # Valor padrão

        if not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "O parâmetro 'url' é obrigatório."})
            }

        response = requests.get(url)
        html_content = response.content

        imagens_sem_alt = analyze_images(html_content, url)

        # Criar a resposta com os resultados
        response_body = {
            "site_name": site_name,
            "url": url,
            "imagens_sem_alt": imagens_sem_alt,
            "message": "Análise completada!"
        }

        return {
            "statusCode": 200,
            "body": response_body  # Resposta direta em JSON
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
