from autogen import Agent
import openai

class AltTextGeneratorAgent(Agent):
    def __init__(self):
        super().__init__()

    def generate_alt_text(self, image_url):
        # Implementação do método generate_alt_text
        prompt = f"Descreva a imagem localizada em {image_url} de forma concisa."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()
