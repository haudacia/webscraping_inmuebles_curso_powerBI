import cloudscraper
from bs4 import BeautifulSoup

endereco = 'https://www.uniqlo.com/es/es/mujer/tops/camisetas-y-polos/camisetas-de-manga-corta?sz=24'

scraper = cloudscraper.create_scraper()
html = scraper.get(endereco).content
soup1 = BeautifulSoup(html, 'html.parser')
precos = soup1.findAll('span', class_="price group product-current-price")
nomes_produtos = soup1.findAll('span', class_="productTile__heading")


artigos = soup1.find_all('article', class_="productTile__heading")

#SO PRECO

def pegar_textos(soup_iteravel):
    lista_textos = []
    for index,item in enumerate(soup_iteravel):
        item_texto = soup_iteravel[index].get_text(strip=True)
        lista_textos.append(item_texto)
    return lista_textos

# Extrair textos para preços e nomes de produtos
lista_precos = pegar_textos(precos)
lista_nomes_produtos = pegar_textos(nomes_produtos)
lista_artigos = pegar_textos(artigos)
print(len(lista_precos))
print(len(lista_nomes_produtos))
print(lista_artigos)
lista_precos = []
for index, item in enumerate(precos, start=0):
    preco_texto = precos[index].get_text()
    lista_precos.append(preco_texto)
# print(lista_precos)

lista_nomes = []
# for index, item in enumerate(nomes_produtos, precos], start=0):
#     for element in item:
#         txt = element.get_text()
#         # print(txt)
#     nome_texto = nomes_produtos[index].get_text()
#     preco_texto = precos[index].get_text()

#tentando aplicar enumerate a lista p fazer ele pegar de uma so vez nome do produto e seu preco respectivo
for index, item in enumerate(nomes_produtos, start=0):
    nome_texto = nomes_produtos[index].get_text()
    lista_nomes.append(nome_texto)
# print(lista_nomes)

#
myDict = {k:v for (k,v) in zip(lista_nomes, lista_precos)}
# print(myDict)
# dict = {nome_texto: preco_texto for n,p in [nomes_produtos,]}
# preco_class = "price group product-current-price"
# nome_class = "productTile__heading"
# # infos = [preco_class, nome_class]
# # for info in infos:
# #     print()
# # [infos_produto = soup1.findAll('span', class_=preco_class)]
# #
# # print(nome_produto, preco)