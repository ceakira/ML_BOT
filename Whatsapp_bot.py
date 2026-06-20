import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from rich.console import Console
from config import MICROSOFT_PROFILE_PATH


console = Console()

class WhatsAppBot:
    def __init__(self, target_name):
        self.target_name = target_name
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 20)

    def _init_driver(self):
        edge_options = Options()
        # Salva a sessão para evitar QR Code todas as vezes
        edge_options.add_argument(f"user-data-dir={MICROSOFT_PROFILE_PATH}")
        # Melhora compatibilidade com Windows e evita detecção básica
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1200,800")
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        return driver

    def open_whatsapp(self):
        self.driver.get("https://web.whatsapp.com")
        console.print("[bold cyan]Aguardando o carregamento do WhatsApp Web...[/bold cyan]")
        console.print("[yellow]Dica: Se o QR Code aparecer, escaneie-o. Se já estiver logado, apenas aguarde.[/yellow]")
        
        # Lista de possíveis seletores para identificar que a página principal carregou
        selectors = [
            '//*[@id="app"]/div/div/div[3]/div/div[3]/header/header/div/span/div/div[2]/span/button/div/div/div[1]/span',
            '//*[@id="_r_a_"]',
            '//*[@id="app"]/div/div/div[3]/div/div[3]/header/header/div/span/div/div[1]/span/div/button/div/div/div[1]/span',
            '//div[@data-testid="chat-list-search"]'
        ]
        
        start_time = time.time()
        while time.time() - start_time < 120:
            for xpath in selectors:
                try:
                    element = self.driver.find_elements(By.XPATH, xpath)
                    if element:
                        console.print(f"[bold green]Conexão estabelecida! (Elemento encontrado via: {xpath})[/bold green]")
                        time.sleep(2) # Pausa para estabilização
                        return
                except:
                    continue
            time.sleep(2)
        
        raise Exception("Não foi possível detectar o carregamento do WhatsApp Web após 120 segundos.")

    def find_contact(self):
        console.print(f"[bold blue]🔍 Buscando contato: {self.target_name}[/bold blue]")
        
        # Seletores baseados na descoberta (focando em <input>)
        search_selectors = [
            '//input[@data-tab="3"]',
            '//input[@aria-label="Pesquisar ou começar uma nova conversa"]',
            '//input[@role="textbox"]',
            '//input[@type="text"]',
            '//input[@class="html-input xdj266r x14z9mp xat24cr x1lziwak xexx8yu x18d9i69 x1c1uobl x14ug900 xjbqb8w x1v8p93f x1o3jo1z x16stqrj xv5lvn5 x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1qx5ct2 xlyipyv xh8yej3 x1uvtmcs x1hcheoe x1nzty39 xkrh14z x1f6kntn xjb2p0i x8r4c90 xo1l8bm x1ic7a3i x12xpedu"]',
            '//input[@autocomplete="off"]'
        ]
        
        search_box = None
        for selector in search_selectors:
            try:
                if "//" in selector:
                    search_box = self.driver.find_element(By.XPATH, selector)
                else:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if search_box.is_displayed():
                    console.print(f"[green]Barra de pesquisa identificada! (via: {selector})[/green]")
                    break
            except:
                continue
            
        if not search_box:
            raise Exception("Não consegui encontrar a caixa de pesquisa. Por favor, clique nela manualmente.")

        search_box.click()
        time.sleep(0.5)
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        
        for char in self.target_name:
            search_box.send_keys(char)
            time.sleep(0.1)
            
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        console.print("[green]Chat aberto![/green]")
        time.sleep(1)

    def send_message(self, message):
        # Tenta encontrar o campo de texto do chat usando padrões similares ao da busca
        input_selectors = [
            '//footer//div[@contenteditable="true"][@role="textbox"]',
            '//div[@role="textbox"]',
            '//br[@data-lexical-managed-linebreak="true"]',
            '//div[@data-tab="10"]',
            '//p[@class="selectable-text copyable-text x15bjb6t x1n2onr6"]' # Fallback caso seja input também
        ]
        
        chat_box = None
        for xpath in input_selectors:
            try:
                if xpath.startswith('//') or xpath.startswith('/*'):
                    chat_box = self.driver.find_element(By.XPATH, xpath)
                else:
                    chat_box = self.driver.find_element(By.CSS_SELECTOR, xpath)
                
                if chat_box: 
                    console.print(f"[green]Campo de mensagem encontrado! (via: {xpath})[/green]")
                    break
            except:
                continue

        if not chat_box:
            raise Exception("Não encontrei o campo de digitação no chat. Tente clicar no campo de texto para ver se o bot assume.")

        # Digita a mensagem
        for char in message:
            chat_box.send_keys(char)
        
        time.sleep(0.5)
        chat_box.send_keys(Keys.ENTER)
        console.print(f"[bold green]✔️ Mensagem enviada para {self.target_name}[/bold green]")

    def get_chat_history(self, limit=5):
        """
        Lê as últimas mensagens do chat aberto.
        """
        # Seletor genérico para os blocos de mensagem no WhatsApp Web novo
        messages = self.driver.find_elements(By.CLASS_NAME, "message-in")
        results = []
        for msg in messages[-limit:]:
            try:
                # Tenta extrair o texto limpo da bolha de conversa
                text = msg.find_element(By.CLASS_NAME, "copyable-text").text
                results.append(text)
            except:
                continue
        return "\n".join(results)

    def close(self):
        self.driver.quit()