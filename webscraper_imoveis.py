import cloudscraper
from bs4 import BeautifulSoup

endereco = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'

scraper = cloudscraper.create_scraper()
html = scraper.get(endereco).content
soup1 = BeautifulSoup(html, 'html.parser')
prices = soup1.findAll('span', class_="item-price h2-simulated")
anuncios = soup1.find_all('article', class_="item")

for item in anuncios:
    #Bloco de string com todas as infos por anuncio:
    infos_completas_por_anuncio = item.find('div', class_="item-info-container")
    # print(infos_completas_por_anuncio.get_text(),'--------------------')
    # UM A UM:
    preco = item.find('span', class_="item-price h2-simulated")
    preco_destrinchado = preco.get_text().split('€')
    preco_numerico = float(preco_destrinchado[0].replace('.',''))
    print(preco_numerico)
    titulo = item.find('div', class_="item-detail-char")
    print(titulo.get_text())


# for index, item in enumerate(infos_item):
#     a_tag = infos_item[index].find('a')
#     titulo = a_tag['title']
#     href_value = a_tag['href']
#     print(a_tag)
#     print(titulo)
#
#     print(href_value)


# anuncios_listagem = soup1.findAll('main')

# o enumerate funciona
# for index, item in enumerate(anuncios, start=0):
#     item_texto = anuncios[index].get_text(strip=True, separator='-')
#     preco = soup1.find('span', class_="item-price h2-simulated")
#     infos = soup1.find('div', class_="item-info-container")
#     titulo = soup1.find('title')
#     # preco_txt = preco.get_text()
#     # print(item_texto)
#     print(titulo.get_text(), preco.get_text())
#     print('----------------------------------------')



## nao entendi pq nao consegui armazenar o get_text como variavel dentro do enumerate acima.
# for index, item in enumerate(infos, start=0):
    # item_texto = infos[index].get_text(strip=True, separator='-')
    #
    # print(item_texto)
    # preco = soup1.find('span', class_="item-price h2-simulated")
    # preco_txt = preco.get_text()
    # titulo = soup1.find('title')
    #
    # print(titulo.get_text(),preco_txt)
    # print('----------------------------------------')



# for index, item in enumerate(prices, start=0):
#     prices_text = prices[index].get_text()
#     print(prices_text)

def coletar_textos(soup_iteravel):
    lista_textos = []
    for index,item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos

# print(prices)
# lista_anuncios = coletar_textos(anuncios)
# print(lista_anuncios)
# for item in lista_artigos:
#     if "€" in item:
#         print(item)
#
# for anuncio in anuncios:
#     preco = soup1.find('span', class_="item-price h2-simulated")
#     print(preco)
