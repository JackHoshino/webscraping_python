import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unicodedata import normalize


#removendo acentuação
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

#contando o nº de divs na pagina
def countDivClass(html, className):
    soup = BeautifulSoup(html.text, 'html.parser')
    count = soup.find_all('div', class_ = className)
    return len(count)


link = 'https://www.meubuzu.com.br/linhas?page='
i=1
totalPag = 25
linhasPorPag = 20
linhasNome = []
linhasCod = []
percursoNome = []
classNameIn = 'col-xs-12 line-item-name'

while(i < totalPag):
    pageOut = requests.get(link + str(i))
    k = 1
    if(pageOut.status_code == 200):
        soupOut = BeautifulSoup(pageOut.text, 'html.parser')
        while(k < linhasPorPag):
            tempCodOut = soupOut.find_all('div', class_ = 'col-lg-2 col-sm-2 col-xs-3 text-center hidden-xs')[k].get_text()
            tempNomeOut = soupOut.find_all('span', class_ = 'hidden-xs')[k].get_text()
            tempIn = soupOut.find_all('div', class_ = 'col-sm-5 col-xs-10')[k]
            linhasCod.append(tempCodOut.replace('\n', ''))
            linhasNome.append(remover_acentos(tempNomeOut))
            strLinkIn = str(tempIn.find('a')['href'])
            pageIn = requests.get(strLinkIn)
            if(pageIn.status_code == 200):
                soupIn = BeautifulSoup(pageIn.text, 'html.parser')
                j = countDivClass(pageIn, classNameIn)
                m = 0
                while(m < j):
                    tempIn = soupIn.find_all(class_ = classNameIn)[m].get_text()
                    percursoNome.append(tempCodOut.replace('\n', '') + '>' + remover_acentos(tempIn.replace('\n', '')))
                    m+=1
            k+=1
            if(i == totalPag):
                k = 20
                break
    i+=1

dfLinhasSite = pd.DataFrame(linhasCod, linhasNome)

dfLinhasSite.to_excel('linhasSite.xls')

