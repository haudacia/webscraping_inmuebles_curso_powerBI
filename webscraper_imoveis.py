import os

import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

inicio_endereco_1 = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'
inicio_endereco_2 = 'https://www.idealista.com/alquiler-viviendas/madrid-madrid/'
inicio_endereco_3 = 'https://www.idealista.com/alquiler-viviendas/cordoba-cordoba/'

webpages_alquiler = [inicio_endereco_1, inicio_endereco_2, inicio_endereco_3]
quant_paginas = 3 #melhorar
fim_endereco = '.htm'

todos_anuncios = []
anuncios_por_cidade = {}
cidades = []

# criando listas de paginas contendo os anuncios por cidade e unindo-as em uma coleção
for pagina_principal in webpages_alquiler:
    nome_cidade = pagina_principal.split('/')[4].split('-')[0]
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
all_titulos = []
all_precos = []
all_quan_habitaciones = []
all_areas = []
all_tipos = []
all_pavtos = []
all_zonas = []
all_ciudades = []
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
        tipo = titulo.split()[0]
        # Separando as informaçoes dadas em forma de texto corrido (str) no html:
        infos_lista = (anuncio.find('div', class_="item-detail-char")).get_text().split()
        try:
            habitaciones = infos_lista[infos_lista.index('hab.')-1]
            pavto = infos_lista[5]
        except:
            pavto = ''
            habitaciones = ''
            pass
        preco_decomp = anuncio.find('span', class_="item-price h2-simulated").get_text().split('€')
        preco = float(preco_decomp[0].replace('.',''))
        area = infos_lista[infos_lista.index('m²') - 1]
        zona = titulo.split(',')[-2] # penultimo item se refere ao bairro ou zona
        ciudad = titulo.split(',')[-1] # ultimo item se refere à cidade
        # print(f'\033[33m€ {preco_numerico:.2f}\033[m')
        # print(detalhes)
        # all_quan_quartos.append(detalhes)
        all_indices.append(index)
        all_titulos.append(titulo)
        all_precos.append(preco)
        all_quan_habitaciones.append(habitaciones)
        all_areas.append(area)
        all_tipos.append(tipo)
        all_pavtos.append(pavto)
        all_zonas.append(zona)
        all_ciudades.append(ciudad)
    ## Conferindo que todas as listas tem a mesma quantidade de itens:
    # print(len(all_indices), len(all_detalhes), len(all_titulos), len(all_precos))
    dict = {'INDICE': all_indices,
            'CIUDAD': all_ciudades,
            'TITULO': all_titulos,
            'TIPO IMOVEL': all_tipos,
            'ZONA': all_zonas,
            'AREA': all_areas,
            'PRECO': all_precos,
            'HAB': all_quan_habitaciones,
            'PAVTO': all_pavtos
            }
    df = pd.DataFrame(dict)
    # df_madrid =
    # df_cordoba =
    df.to_excel('anuncios_alquiler_espanha0.xlsx')
        # with pd.ExcelWriter('anuncios_alquiler_espanha.xlsx') as writer:
        #     df.to_excel(writer, sheet_name=cidades[0])

        # df.to_excel(writer, sheet_name=cidades[1])
        # df.to_excel(writer, sheet_name=cidades[2])
    # df_1 = pd.DataFrame(dict)
    # df_1.to_excel('df_1.xlsx')
    # os.startfile('df_1.xlsx')
# coletando todas as páginas de todas as cidades.
# for endereco in webpages_alquiler:
#     coletar_dados_organizados(endereco)
for p in todos_anuncios:
    for item in p:
        coletar_dados_organizados(item)

os.startfile('anuncios_alquiler_espanha0.xlsx')

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