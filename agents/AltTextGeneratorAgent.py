import openai

class AltTextGeneratorAgent:
    def __init__(self):
        super().__init__()
        openai.api_key = "sua_chave_api_aqui"  # Adicione sua chave API aqui

    def generate_alt_text(self, image_url):
        # Implementação do método generate_alt_text com a nova interface da API
        prompt = f"Descreva a imagem localizada em {image_url} de forma concisa."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Utilize o modelo correto aqui
            messages=[
                {"role": "system", "content": "Você é um gerador de descrições de imagens."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
