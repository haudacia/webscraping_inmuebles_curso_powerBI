import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

inicio_endereco_1 = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'
inicio_endereco_2 = 'https://www.idealista.com/alquiler-viviendas/madrid-madrid/'
inicio_endereco_3 = 'https://www.idealista.com/alquiler-viviendas/cordoba-cordoba/'

webpages_alquiler = [inicio_endereco_1, inicio_endereco_2, inicio_endereco_3]
quant_paginas = 10
fim_endereco = '.htm'

conjunto_anuncios_cidades = []
for pagina_1 in webpages_alquiler:
    variavel_cidade = pagina_1.split('/')[4]
    nome_cidade = variavel_cidade.split('-')[0]
    todas_paginas_cidade = [pagina_1]

    for i in range(quant_paginas):
        if i >= 2:
            endereco_completo = pagina_1 + f'pagina-{i}' + fim_endereco
            todas_paginas_cidade.append(endereco_completo)
    conjunto_anuncios_cidades.append(todas_paginas_cidade)
print(conjunto_anuncios_cidades)

# inicio =

# Turn all this below into a function so I can use it to any address (in idealista, at least)
def coletar_dados_organizados(endereco):
    # endereco = input('Insira o endereço completo da página')

    scraper = cloudscraper.create_scraper()
    html = scraper.get(endereco).content
    soup1 = BeautifulSoup(html, 'html.parser')
    anuncios = soup1.find_all('article', class_="item")

    for index, anuncio in enumerate(anuncios, start=1):
        #Bloco de string com todas as infos por anuncio:
        infos_completas_por_anuncio = anuncio.find('div', class_="item-info-container")
        titulo = infos_completas_por_anuncio.find('a', class_="item-link")
        print(f'\033[35;7m{index} - {titulo.get_text().strip()}\033[m')
        # UM A UM:
        detalhes = (anuncio.find('div', class_="item-detail-char")).get_text().strip()
        preco = anuncio.find('span', class_="item-price h2-simulated")
        preco_decomp = preco.get_text().split('€')
        preco_numerico = float(preco_decomp[0].replace('.',''))
        print(f'\033[33m€ {preco_numerico:.2f}\033[m')
        print(detalhes)
        # dict = {index: [titulo,preco_numerico,detalhes]}
        # print(dict)
    print(len(anuncios))
# for p in webpages_alquiler:
#     coletar_dados_organizados(p)

# Funçâo para coletar apenas textos dos objetos bs4 (não foi necessária a partir de quando se descobriu o item certo que
# armazena cada anuncio. A ideia era coletar separadamente as listas de precos, titulos, area e depois referencia-las
# de novo a seus respectivos anuncios a partir de seus indices em comum.

def coletar_textos(soup_iteravel):
    lista_textos = []
    for index, item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos