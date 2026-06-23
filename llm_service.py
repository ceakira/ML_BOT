import requests
from config import LLM_API_URL
from Price_bot import ScrapeAndPrint
import emoji
import re

class LLMService:
    
    # Emojis seguros para WhatsApp com seus códigos
    WHATSAPP_SAFE_EMOJIS = {
    "🏪": ":24",
    "🎟": ":admission",
    "🛫": ":airplane",
    "🚑": ":ambulance",
    "🎡": ":amusementpark",
    "🎢": ":amusementpark",
    "✳": ":asterisk",
    "⚛": ":atom",
    "🛄": ":baggage",
    "🔋": ":battery",
    "💜": ":bestest",
    "🧔🏻": ":bewhiskered",
    "☣": ":biohazard",
    "🥊": ":boxing",
    "🧠": ":brain",
    "🥦": ":broccoli",
    "💔": ":broken",
    "🛶": ":canoe",
    "⛓": ":chains",
    "💺": ":chair",
    "✅": ":checkmark",
    "✔": ":checkmark",
    "🚆": ":choo",
    "🚬": ":cigarette",
    "🎪": ":tent",
    "😙": ":closed",
    "⚰": ":coffin",
    "🆒": ":cool",
    "🚁": ":copter",
    "©": ":copyright",
    "❎": ":cross_mark",
    "🚸": ":crossing",
    "💘": ":heart",
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
    "🚒": ":fire",
    "🆓": ":free",
    "⛽": ":fuel",
    "⚱": ":funeral",
    "🤭": ":giggle",
    "🦒": ":giraffe",
    "🥍": ":goal",
    "🥅": ":goal",
    "💚": ":green",
    "🎸": ":guitar",
    "#⃣": ":hashtag",
    "💝": ":heart",
    "💓": ":heartbeat",
    "💗": ":heartpulse",
    "🦔": ":hedgehog",
    "🛣": ":highway",
    "🤗": ":hugging",
    "🆔": ":id",
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
    "🛤": ":railway",
    "♻": ":recycle",
    "❤": ":red",
    "®": ":registered",
    "🎗": ":reminder",
    "💞": ":revolving",
    "🌹": ":rose",
    "🏵": ":rose",
    "⛵": ":sailboat",
    "🦕": ":sauropod",
    "🎷": ":sax",
    "🛵": ":scooter",
    "🛴": ":scooter",
    "🤫": ":shushing",
    "🎚": ":slider",
    "😍": ":smiling",
    "🧦": ":sock",
    "💖": ":sparkling",
    "🤮": ":spew",
    "🕸": ":spider",
    "🎏": ":streamer",
    "🚟": ":suspension",
    "🦖": ":t-rex",
    "⛺": ":tent",
    "🤔": ":thinkinge",
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
    "💛": ":yellow",
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
           Você é um Copywriter especialista em WhatsApp. Transforme dados brutos em mensagens persuasivas, garantindo a formatação exata para o aplicativo.

            # DADOS RECEBIDOS:
            titulo, link, highlight, avaliacao, preco, frete, desconto

            # ESTRUTURA E FORMATAÇÃO OBRIGATÓRIA:
            (Reproduza a estrutura abaixo rigorosamente. Mantenha os asteriscos '*' exatamente onde estão para ativar o negrito no WhatsApp. Substitua a tag (emoji) por itens da lista permitida).

            (emoji) *[highlight]* (emoji) (Se vazio, use: (emoji) *OFERTA RELÂMPAGO* (emoji))

            (emoji) *[titulo]*

            (emoji) *[preco]* [Se houver desconto: (*[desconto]*)]
            (emoji) [frete] (Se vazio, exclua a linha)
            (emoji) [avaliacao] (Se vazio, exclua a linha)

            [Crie UMA frase curta e persuasiva gerando urgência] (emoji)

            [link]

            # REGRAS RÍGIDAS (LEIA COM ATENÇÃO):
            1. NEGRITO (CRÍTICO): É estritamente proibido remover os asteriscos '*'. Eles são essenciais para o layout do WhatsApp.
            2. EMOJIS: Onde houver a marcação "(emoji)", você DEVE escolher um emoji que faça sentido para a linha, usando ÚNICA e EXCLUSIVAMENTE esta lista: {LLMService.WHATSAPP_SAFE_EMOJIS}.
            3. ZERO RÓTULOS: Não escreva "Nome do Produto", "Preço:" ou "Detalhes".
            4. TRATAMENTO DE PREÇO: Se o preço vier quebrado ou com um "R" solto, não tente consertar ou explicar. Apenas coloque a informação exatamente como recebeu.
            5. ESPAÇAMENTO: Mantenha as quebras de linha reais do template (use Enter).

            # REGRA CRÍTICA DE SAÍDA:
            Retorne APENAS a mensagem final, pronta para envio. Nenhuma palavra a mais.
            """
        )
        
        payload = {
            "system": system_prompt,     # Chave corrigida para minúsculo
            "model": "llama3",
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
        texto_final = ""
        resposta_ia = LLMService.generate_response_options(message_product)  # Para teste, processa apenas o primeiro produto. Pode ser expandido para todos.
        
        # Restringe apenas aos emojis seguros do WhatsApp
        texto = LLMService.restrict_to_whatsapp_emojis(resposta_ia)
        for i, char in enumerate(texto):
            if char == "\n":
                    texto_final += "@"
            else:
                    texto_final += char

            continue # Pula para a próxima letra do laço


        return texto_final
            # 3. Exibe a mensagem formatada pela IA (pode ser enviada para
            # print("=== MENSAGEM GERADA PARA O WHATSAPP ===")
            # print(resposta_ia)
            # print("=======================================\n")
    

  