import os
from selenium import webdriver

if os.environ['PATH'].find(';C:\\SeleniumDrivers') > 0:
    pass
else:
  os.environ['PATH'] += ";C:\\SeleniumDrivers"

driver = webdriver.Chrome()
driver.implicitly_wait(~2) # or another adequate time
driver.get('https://www.yoursitegoeshere.com')

with open("https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/.html", "w", encoding='utf8') as f:
    f.write(driver.page_source)

import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

inicio_endereco_1 = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'
inicio_endereco_2 = 'https://www.idealista.com/alquiler-viviendas/madrid-madrid/'
inicio_endereco_3 = 'https://www.idealista.com/alquiler-viviendas/cordoba-cordoba/'

webpages_alquiler = [inicio_endereco_1, inicio_endereco_2, inicio_endereco_3]
quant_paginas = 6 #melhorar
fim_endereco = '.htm'

todos_anuncios = []
anuncios_por_cidade = {}
cidades = []

# criando listas de paginas contendo os anuncios por cidade e unindo-as em uma coleção
for pagina_principal in webpages_alquiler:
    variavel_cidade = pagina_principal.split('/')[4]
    nome_cidade = variavel_cidade.split('-')[0]
    cidades.append(nome_cidade)
    paginas_cidade = [pagina_principal]

    for i in range(2,quant_paginas):
        endereco_completo = pagina_principal + f'pagina-{i}' + fim_endereco
        paginas_cidade.append(endereco_completo)
    todos_anuncios.append(paginas_cidade)
    # permitindo acessar, fora do loop, as listas de paginas por cada cidade em separado
    anuncios_por_cidade.update({nome_cidade: paginas_cidade})
    # print(paginas_cidade)
# print(todos_anuncios)
all_indices = []
all_detalhes = []
all_titulos = []
all_precos = []
dict = {}
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
        titulo_decomp = infos_completas_por_anuncio.find('a', class_="item-link")
        titulo = titulo_decomp.get_text().strip()

        # print(f'\033[35;7m{index} - {titulo.get_text().strip()}\033[m')
        # UM A UM:
        detalhes = (anuncio.find('div', class_="item-detail-char")).get_text().strip()
        preco_decomp = anuncio.find('span', class_="item-price h2-simulated").get_text().split('€')
        preco = float(preco_decomp[0].replace('.',''))
        # print(f'\033[33m€ {preco_numerico:.2f}\033[m')
        # print(detalhes)
        all_indices.append(index)
        all_detalhes.append(detalhes)
        all_titulos.append(titulo)
        all_precos.append(preco)
    ## Conferindo que todas as listas tem a mesma quantidade de itens:
    # print(len(all_indices), len(all_detalhes), len(all_titulos), len(all_precos))
    dict = {'INDICE': all_indices,
            'NOME': all_titulos,
            'PRECO': all_precos,
            'DETALHES': all_detalhes
            }
    df = pd.DataFrame(dict)
    df.to_excel('test7.xlsx')
        # with pd.ExcelWriter('test1.xlsx') as writer:
        #     df.to_excel(writer, sheet_name=cidades[0])

        # df.to_excel(writer, sheet_name=cidades[1])
        # df.to_excel(writer, sheet_name=cidades[2])
    # df_1 = pd.DataFrame(dict)
    # df_1.to_excel('df_1.xlsx')
    # os.startfile('df_1.xlsx')
# coletando todas as páginas de todas as cidades.
# for endereco in webpages_alquiler:
#     coletar_dados_organizados(endereco)
print(all_indices)

for p in todos_anuncios:
    for item in p:
        print(item)
        coletar_dados_organizados(item)
# os.startfile('test1.xlsx')
# Funçâo para coletar apenas textos dos objetos bs4 (não foi necessária a partir de quando se descobriu o item certo que
# armazena cada anuncio. A ideia era coletar separadamente as listas de precos, titulos, area e depois referencia-las
# de novo a seus respectivos anuncios a partir de seus indices em comum.

def coletar_textos(soup_iteravel):
    lista_textos = []
    for index, item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos