import requests
from config import LLM_API_URL
from Price_bot import ScrapeAndPrint
import emoji
import re

class LLMService:
    
    # Emojis seguros para WhatsApp com seus códigos
    WHATSAPP_SAFE_EMOJIS = {
    "🔞": ":18",
    "🏪": ":24",
    "🎟": ":admission_ticket",
    "🛬": ":airplane_arrival",
    "🛫": ":airplane_departure",
    "🚑": ":ambulance",
    "🎡": ":amusementpark",
    "🎢": ":amusementpark",
    "✳": ":asterisk",
    "⚛": ":atom",
    "🛄": ":baggage_claim",
    "🔋": ":battery",
    "💜": ":bestest",
    "🧔🏻": ":bewhiskered",
    "☣": ":biohazard",
    "💙": ":blue_heart",
    "🥊": ":boxing",
    "🧠": ":brain",
    "🥦": ":broccoli",
    "💔": ":broken",
    "🛶": ":canoe",
    "⛓": ":chains",
    "💺": ":chair",
    "✅": ":checkmark",
    "✔": ":checkmark",
    "🚆": ":choo_choo",
    "🚬": ":cigarette",
    "🎪": ":tent",
    "😙": ":closed_eyes",
    "⚰": ":coffin",
    "🆒": ":cool_button",
    "🚁": ":copter",
    "©": ":copyright",
    "❎": ":cross_mark",
    "🚸": ":crossing",
    "💘": ":heart_with_arrow",
    "🛃": ":customs",
    "🤨": ":distrust",
    "🥁": ":drumsticks",
    "🥟": ":dumpling",
    "🤯": ":explode",
    "💥": ":explode",
    "😘": ":lover",
    "💯": ":faith",
    "🤺": ":fencer",
    "⛴": ":ferry",
    "🚒": ":fire_engine",
    "🆓": ":free_button",
    "⛽": ":fuel_pump",
    "⚱": ":funeral",
    "🤭": ":giggle",
    "🦒": ":giraffe",
    "🥍": ":goal",
    "🥅": ":goal",
    "💚": ":green_heart",
    "🎸": ":guitar",
    "#⃣": ":hashtag",
    "💝": ":heart_with_ribbon",
    "💓": ":heartbeat",
    "💗": ":heartpulse",
    "🦔": ":hedgehog",
    "🛣": ":highway",
    "🤗": ":hugging_face",
    "🆔": ":id_button",
    "✈": ":jet",
    "🥋": ":judo",
    "🎛": ":knobs",
    "🗽": ":liberty",
    "🚂": ":locomotive",
    "💌": ":love_letter",
    "🧜‍": ":triton",
    "🚇": ":metro",
    "🎤": ":microphone",
    "🎙": ":microphone",
    "🖕": ":middle",
    "🎖": ":military",
    "🚤": ":millionaire",
    "🚐": ":minibus",
    "🚝": ":mono",
    "🚈": ":mono",
    "🤶": ":mother",
    "🛥": ":motorboat",
    "💅🏻": ":nail",
    "🆕": ":new_button",
    "🚭": ":no_smoking",
    "🛢": ":oil",
    "🖌": ":paintbrush",
    "🅿": ":parking",
    "🛂": ":passport",
    "😇": ":peaceful",
    "☮": ":peaceful",
    "🐧": ":penguin",
    "🎹": ":piano",
    "🤬": ":pissed",
    "😒": ":pissed",
    "🔌": ":plug",
    "🥨": ":pretzel",
    "🥠": ":prophecy",
    "☢": ":radioactive",
    "🛤": ":railway_track",
    "♻": ":recycle",
    "❤": ":red_heart",
    "®": ":registered",
    "🎗": ":reminder",
    "💞": ":revolving_hearts",
    "🌹": ":rose",
    "🏵": ":rose",
    "⛵": ":sailboat",
    "🦕": ":sauropod",
    "🎷": ":sax",
    "🛵": ":scooter",
    "🛴": ":scooter",
    "🤫": ":shushing_face",
    "🎚": ":slider",
    "😍": ":smiling_face_with_heart",
    "🧦": ":sock",
    "💖": ":sparkling_heart",
    "🤮": ":spew",
    "🕸": ":spider_web",
    "🎏": ":streamer",
    "🚟": ":suspension",
    "🦖": ":t-rex",
    "⛺": ":tent",
    "🤔": ":thinking_face",
    "🙏": ":thx",
    "🧕": ":tichel",
    "🚢": ":titanic",
    "🗼": ":tokyo",
    "🚜": ":tractor",
    "🎺": ":trumpet",
    "💕": ":two_hearts",
    "🔑": ":unlock",
    "🔓": ":unlock",
    "🆚": ":versus",
    "🎻": ":violin",
    "⚠": ":warning",
    "🗑": ":waste",
    "♿": ":wheelchair",
    "💟": ":white_heart",
    "💛": ":yellow_heart",
    "🦓": ":zebra"
    }
    
    @staticmethod
    def restrict_to_whatsapp_emojis(text):
        """
        Restringe a mensagem apenas aos emojis seguros do WhatsApp.
        Converte emojis permitidos para seus códigos (:fire:, :rocket:, etc).
        Remove emojis não permitidos.
        """
        if not text:
            return text
        
        resultado = text
        
        # Substitui apenas emojis seguros pelos seus códigos
        for emoji_char, codigo in LLMService.WHATSAPP_SAFE_EMOJIS.items():
            resultado = resultado.replace(emoji_char, codigo)
        
        # Remove qualquer emoji restante (não autorizado)
        # Padrão regex para detectar emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Símbolos e pictogramas
            "\U0001F680-\U0001F6FF"  # Transporte
            "\U0001F700-\U0001F77F"  # Dingbats
            "\U0001F780-\U0001F7FF"  # Geometria
            "\U0001F800-\U0001F8FF"  # Dingbats suplementares
            "\U0001F900-\U0001F9FF"  # Símbolos suplementares
            "\U0001FA00-\U0001FA6F"  # Xadrez
            "\U0001FA70-\U0001FAFF"  # Símbolos suplementares
            "\U00002500-\U00002BEF"  # Símbolos chineses
            "\U0001F1E0-\U0001F1FF"  # Bandeiras
            "]+"
        )
        
        resultado = emoji_pattern.sub('', resultado)
        return resultado
    
    @staticmethod
    # def products_format_message():
    #     mensagens_formatadas = []
        
    #     # Cria uma lista de strings com o formato básico
    #     for produto in produtos:
    #         titulo = produto["titulo"]
    #         link = produto["link"]
    #         mensagem = f"Produto: {titulo}\nLink: {link}\n"
    #         mensagens_formatadas.append(mensagem)
        
    #     return mensagens_formatadas

    @staticmethod
    def generate_response_options(dados_do_produto):        
        """
        Envia os dados de UM produto para o Ollama local e gera a copy.
        """
        system_prompt = (
            f"""
            Você é um especialista em copywriting e marketing digital, focado em conversão e vendas pelo WhatsApp.
            Seu trabalho é atuar como um formatador automático: você receberá dados brutos de uma promoção enviados por um sistema, e sua única função é transformar esses dados em uma mensagem de WhatsApp altamente atrativa e persuasiva.

            REGRAS DE FORMATAÇÃO E ESTILO:
            1. Gancho Inicial: Comece sempre com um alerta chamativo que prenda a atenção imediatamente 
            2. Destaque o Valor: Use negrito do WhatsApp (*texto*) para enfatizar o nome do produto.
            3. Gatilhos Mentais: Gere senso de urgência ou exclusividade no texto.
            4. Link de Compra: Inclua o link de compra no final da mensagem, sempre precedido por uma chamada clara para ação (ex: "Confira aqui: [link]").
            5. Estrutura Arejada: Use quebras de linha entre as frases.
            6. Call to Action (CTA): Finalize sempre com uma chamada de ação clara apontando para o link de compra.
            7. Máximo de 2-3 emojis por mensagem para melhor visualização no WhatsApp Web.
            8. a mensagem deve ser curta e direta, com no máximo 4 linhas de texto (sem contar o link).
            9. Envie o texto formatado em uma so mensagem, sem dividir em partes.
            10.use os emojis que estao em {LLMService.WHATSAPP_SAFE_EMOJIS.values()} para deixar a mensagem mais atrativa, mas SEM EXAGEROS (máximo de 2-3 por mensagem).
            11. use somente pt-br
            12. evite usar barra invertida + n para fazer a quebra de linha, voce deve fazer essa quebra de linha manualmente
            13. um exemplo bom de formatacao: 
            ⚠️ Oferta relâmpago com estoque quase zerado!

            Leve a sua *Smart TV 55" 4K Samsung* com 40% OFF agora.

            Últimas 3 unidades com entrega Full gratuita, vai esgotar em minutos.

            Garanta a sua antes que o preço suba clicando aqui ⬇️
            https://produto.mercadolivre.com.br/oferta-tv55

            REGRA ESTRITA DE SAÍDA:
            Você é um bot de processamento em backend. NUNCA inicie sua resposta com saudações, não converse, não diga "Aqui está sua mensagem". Retorne ÚNICA e EXCLUSIVAMENTE o texto final da promoção.
            """
        )
        
        payload = {
            "system": system_prompt,     # Chave corrigida para minúsculo
            "model": "mistral",
            "prompt": dados_do_produto,  # Agora passa a variável corretamente sem aspas
            "stream": False,
            "options": {
                "temperature": 0.4,      # Temperatura levemente maior para melhor copywriting
                "num_predict": 500,      # Aumentado para garantir que a mensagem não corte no meio
                "stop": ["[/INST]", "</s>"]
            }
        }

        try:
            response = requests.post(LLM_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            
            # Pega a resposta em texto puro
            content = response.json().get("response", "")
            return content.strip() # Remove espaços extras nas pontas
            
        except Exception as e:
            return f"Erro ao comunicar com Ollama: {str(e)}"


    def main(message_product):
        print(f"Processando produto {message_product}\n")
        # 1. Busca os produtos e formata em texto
       # mensagens = LLMService.products_format_message()
        
        # 2. Passa cada produto pela IA para gerar a mensagem de WhatsApp
            
        resposta_ia = LLMService.generate_response_options(message_product)  # Para teste, processa apenas o primeiro produto. Pode ser expandido para todos.
        
        # Restringe apenas aos emojis seguros do WhatsApp
        texto_final = LLMService.restrict_to_whatsapp_emojis(resposta_ia)
        print(texto_final)
        return texto_final
            # 3. Exibe a mensagem formatada pela IA (pode ser enviada para
            # print("=== MENSAGEM GERADA PARA O WHATSAPP ===")
            # print(resposta_ia)
            # print("=======================================\n")
    

  