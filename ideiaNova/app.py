from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Função que analisa o HTML em busca de imagens sem texto alternativo
def analyze_images(html, site_url):
    soup = BeautifulSoup(html, 'html.parser')
    imagens_sem_alt = []

    for img in soup.find_all('img'):
        alt_text = img.get('alt')
        img_url = img.get('src')

        # Caso o atributo alt esteja ausente ou vazio
        if not alt_text or alt_text.strip() == "":
            # Gerar um texto alternativo simples (você pode personalizar isso)
            # alt_text_gerado = f"Imagem do site {site_url}"
            
            # Adiciona informações da imagem à lista
            imagens_sem_alt.append({
                'site_url': site_url,
                'img_url': img_url,
                'tag_completa': str(img)
            })

    return imagens_sem_alt

@app.route('/analyze', methods=['POST'])
def analyze_images_route():
    data = request.get_json()
    site_name = data.get('site_name')
    url = data.get('url')

    # Fazendo uma requisição para obter o HTML do site
    try:
        response = requests.get(url)
        html_content = response.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Analisando o HTML para buscar imagens sem alt
    imagens_sem_alt = analyze_images(html_content, url)

    response = {
        "site_name": site_name,
        "url": url,
        "imagens_sem_alt": imagens_sem_alt,
        "message": "Análise completada!"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
