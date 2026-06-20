import requests
from bs4 import BeautifulSoup
import time

# User Agent atualizado
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
        tags_descricao = site.find_all('h3', class_='poly-component__title-wrapper')
        tags_links = site.find_all('a', class_="poly-component__title")
        tags_images = site.find_all('img', class_='poly-component__picture')
        
        # Se não encontrar títulos, encerra
        if not tags_descricao:
            print("Nenhum produto encontrado nesta página. Fim das ofertas.")
            break
            
        print(f"Sucesso! Encontrados {len(tags_descricao)} produtos na página {pagina_atual}.")
        print("-" * 40)
        
        # 2. O ZIP junta a lista de títulos e a lista de links na mesma iteração
        for tag_titulo, tag_link, tag_images in zip(tags_descricao, tags_links, tags_images):
            titulo = tag_titulo.get_text(strip=True)
            
            # Pega o atributo 'href' da tag <a> de forma segura
            link = tag_link.get('href', 'Link não encontrado')
            # Pega o atributo 'src' da tag <img> de forma segura
            # Adicionar o desconto
            print(f"📌 {titulo}")
            print(f"🔗 {link}")
            print(f"🖼️ {tag_images.get('src', 'Imagem não encontrada')}")
            print("-" * 20)
            
        print("-" * 40)
        
        # Avança para a próxima página
        if pagina_atual >= 3:  # Limite de páginas para evitar bloqueios
            break
        pagina_atual += 1
        
        # Pausa recomendada para evitar bloqueios
        time.sleep(3) 
        
    except Exception as e:
        print(f"Ocorreu um erro na requisição: {e}")
        break