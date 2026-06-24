import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import Price_bot
from Whatsapp_bot import WhatsAppBot
from config import FRIEND_NAME, INITIAL_GREETING
from Price_bot import ScrapeAndPrint
from llm_service import LLMService


console = Console()

def main():

    
    console.print(Panel.fit("🤖 Bot de Atendimento WhatsApp (MVP)", style="bold blue"))

    
    bot = WhatsAppBot(FRIEND_NAME)
    
    try:
        bot.open_whatsapp()
        
        # Inicia a conversa
        bot.find_contact()
        count = 0
        for pagina in range(1, 21):
            product_data = ScrapeAndPrint(pagina)

            # Envia cada produto coletado
            for produto in product_data:
                titulo = produto["titulo"]
                link = produto["link"]
                preco = produto["preco"]
                highlight = produto["highlight"]
            #frete = produto["frete"]
                off = produto["discount"]
                

                # Corrigir a passagem de dados para a função de geração de resposta, agora passando o título e link formatados
                message_product = f"Produto: {titulo} Link: {link} preco: {preco} highlight: {highlight}  desconto: {off}"
                message = LLMService.main(message_product)


                count += 1
                bot.send_message(message)
                time.sleep(100)  # Pausa para evitar envio muito rápido


    except Exception as e:
        console.print(f"[bold red]Erro fatal na orquestração:[/bold red] {str(e)}")
    finally:
        bot.close()
        console.print("[bold red]Bot finalizado.[/bold red]")

if __name__ == "__main__":
    main()