import cloudscraper
from bs4 import BeautifulSoup

endereco = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'

scraper = cloudscraper.create_scraper()
html = scraper.get(endereco).content
soup1 = BeautifulSoup(html, 'html.parser')
anuncios = soup1.find_all('article', class_="item")

# Funçâo para coletar apenas textos dos objetos bs4 (não foi necessária a partir de quando se descobriu o item certo que
# armazena cada anuncio. A ideia era coletar separadamente as listas de precos, titulos, area e depois referencia-las
# de novo a seus respectivos anuncios a partir de seus indices em comum.

def coletar_textos(soup_iteravel):
    lista_textos = []
    for index,item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos

for index, anuncio in enumerate(anuncios, start=1):
    #Bloco de string com todas as infos por anuncio:
    infos_completas_por_anuncio = anuncio.find('div', class_="item-info-container")
    titulo = infos_completas_por_anuncio.find('a', class_="item-link")
    print(f'{index} - {titulo.get_text().strip()}')
    # UM A UM:
    detalhes = anuncio.find('div', class_="item-detail-char")
    preco = anuncio.find('span', class_="item-price h2-simulated")
    preco_decomp = preco.get_text().split('€')
    preco_numerico = float(preco_decomp[0].replace('.',''))
    print(f'€ {preco_numerico:.2f}')
    print(detalhes.get_text().strip())
    dict = {}

# o enumerate funcionando:
# for index, item in enumerate(anuncios, start=0):
#     item_texto = anuncios[index].get_text(strip=True, separator='-')
#     preco = soup1.find('span', class_="item-price h2-simulated")
#     infos = soup1.find('div', class_="item-info-container")
#     titulo = soup1.find('title')
#     # preco_txt = preco.get_text()
#     # print(item_texto)
#     print(titulo.get_text(), preco.get_text())
#     print('----------------------------------------')
