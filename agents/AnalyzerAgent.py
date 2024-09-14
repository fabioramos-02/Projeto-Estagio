from bs4 import BeautifulSoup
from agents.AltTextGeneratorAgent import AltTextGeneratorAgent

class AnalyzerAgent:
    def __init__(self):
        self.alt_text_generator = AltTextGeneratorAgent()

    def analyze(self, html, site_url):
        """Analisa o HTML em busca de imagens sem atributo alt e gera textos alternativos."""
        soup = BeautifulSoup(html, 'html.parser')
        imagens_sem_alt = []

        for img in soup.find_all('img'):
            alt_text = img.get('alt')
            img_url = img.get('src')

            # Caso o atributo alt esteja ausente ou vazio
            if not alt_text or alt_text.strip() == "":
                # Gera texto alternativo usando o AltTextGeneratorAgent
                alt_text_gerado = self.alt_text_generator.generate_alt_text(img_url)
                
                # Adiciona informações da imagem à lista
                imagens_sem_alt.append({
                    'site_url': site_url,  # URL do site
                    'img_url': img_url,
                    'alt_text_gerado': alt_text_gerado,
                    'alt_text_original': alt_text,  # Pode ser None ou vazio
                    'tag_completa': str(img)  # Salva a tag completa como string para auditoria
                })

            # Caso o alt exista, mas esteja vazio ou sem sentido (ex: alt="imagem")
            elif alt_text.lower() in ["imagem", "foto", ""]:
                # Também gera um novo texto alternativo para esse caso
                alt_text_gerado = self.alt_text_generator.generate_alt_text(img_url)

                imagens_sem_alt.append({
                    'site_url': site_url,  # URL do site
                    'img_url': img_url,
                    'alt_text_gerado': alt_text_gerado,
                    'alt_text_original': alt_text,
                    'tag_completa': str(img)  # Salva a tag completa como string para auditoria
                })

        return imagens_sem_alt
