import openai
from dotenv import load_dotenv
import os

class AltTextGeneratorAgent:
    def __init__(self):
        # Carrega as variáveis do arquivo .env
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Carrega a chave API da variável de ambiente

    def generate_alt_text(self, image_url):
        # Verifica se o image_url é válido
        if not image_url or not image_url.startswith("http"):
            return "URL da imagem inválida."

        # Prompt otimizado para gerar descrições concisas e eficientes
        prompt = f"Descreva de forma sucinta a imagem localizada em {image_url}."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Gere uma breve descrição da imagem."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50  # Limita o número de tokens para reduzir o custo
            )
            return response['choices'][0]['message']['content'].strip()

        except Exception as e:
            return f"Erro ao gerar descrição: {str(e)}"
