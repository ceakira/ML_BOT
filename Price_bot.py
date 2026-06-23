import requests
from bs4 import BeautifulSoup
import time

# User Agent atualizado

def ScrapeAndPrint():
    produtos_lista = []  # Lista para armazenar todos os produtos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    url_base = "https://www.mercadolivre.com.br/ofertas"
    produtos_por_pagina = 48
    pagina_atual = 1


    while True:
        if pagina_atual == 1:
            url_final = url_base
        else:
            desde = ((pagina_atual - 1) * produtos_por_pagina) + 1
            url_final = f"{url_base}?page={pagina_atual}"

        print(f"Acessando: {url_final}")
        
        try:
            response = requests.get(url_final, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Erro ao acessar a página (Status {response.status_code}). Encerrando.")
                break
                
            site = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Captura as listas de títulos e links usando as classes corretas do ML
            tags_titulo = site.find_all('h3', class_='poly-component__title-wrapper')
            tags_links = site.find_all('a', class_="poly-component__title")
            tags_highlightML = site.find_all('span', class_="poly-component__highlight")
            tags_shipping = site.find_all('div', class_="poly-component__shipping")
            tags_price = site.find_all('span', class_="andes-money-amount andes-money-amount--cents-superscript")
            tags_discount = site.find_all('span', class_="poly-price__disc_label andes-money-amount__discount poly-price__disc_label--pill")
            
            # Se não encontrar títulos, encerra
            if not tags_titulo:
                print("Nenhum produto encontrado nesta página. Fim das ofertas.")
                break
                
            print(f"Sucesso! Encontrados {len(tags_titulo)} produtos na página {pagina_atual}.")
            print("-" * 40)

            produtos_lista = []

# Encaixando tudo no zip:
            for tag_titulo, tag_link, tag_high, tag_preco, tag_frete, tag_disc in zip(tags_titulo, tags_links, tags_highlightML,  tags_price, tags_shipping, tags_discount):
                
                            titulo = tag_titulo.get_text(strip=True)
                            link = tag_link.get('href', 'Link não encontrado')
                            highlight = tag_high.get_text(strip=True) if tag_high else ""
                            preco = tag_preco.get_text(strip=True)
                            frete = tag_frete.get_text(strip=True)
                            off = tag_disc.get_text(strip=True)
                                
                            # Adiciona o produto à lista como um dicionário
                            produtos_lista.append({
                                "titulo": titulo,
                                "link": link,
                                "highlight": highlight,
                                "preco": preco,
                                "frete": frete,
                                "discount": off
                            })
                            
                            if len(produtos_lista) == 3:
                                break

            print(produtos_lista)

                
                
            print("-" * 40)
            
            # Avança para a próxima página
            if pagina_atual >= 1:  # Limite de páginas para evitar bloqueios
                break
            pagina_atual += 1
            
            # Pausa recomendada para evitar bloqueios
            time.sleep(3) 
            
        except Exception as e:
            print(f"Ocorreu um erro na requisição: {e}")
            break
    
    # Retorna a lista com todos os produtos coletados
    return produtos_lista

if __name__ == "__main__":
    ScrapeAndPrint()