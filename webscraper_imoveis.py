import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

inicio_endereco_1 = 'https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/'
inicio_endereco_2 = 'https://www.idealista.com/alquiler-viviendas/madrid-madrid/'
inicio_endereco_3 = 'https://www.idealista.com/alquiler-viviendas/cordoba-cordoba/'

webpages_alquiler = [inicio_endereco_1, inicio_endereco_2, inicio_endereco_3]
quant_paginas = 20 #melhorar
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

print(todos_anuncios)
d = {'NOME': cidades}
df = pd.DataFrame(d)
print(df)


# Turn all this below into a function so I can use it to any address (in idealista, at least)
def coletar_dados_organizados(endereco):
    # endereco = input('Insira o endereço completo da página')
    endereco = endereco
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


# # coletando todas as páginas de todas as cidades.
# for p in todos_anuncios:
#     for item in p:
#         coletar_dados_organizados(item)

df.to_excel('test.xlsx', sheet_name=nomes_cidades[0])


# Funçâo para coletar apenas textos dos objetos bs4 (não foi necessária a partir de quando se descobriu o item certo que
# armazena cada anuncio. A ideia era coletar separadamente as listas de precos, titulos, area e depois referencia-las
# de novo a seus respectivos anuncios a partir de seus indices em comum.








def coletar_textos(soup_iteravel):
    lista_textos = []
    for index, item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos