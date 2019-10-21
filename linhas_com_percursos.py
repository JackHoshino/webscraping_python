import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unicodedata import normalize

#removendo acentuação
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def countDivClass(html, className):
    soup = BeautifulSoup(html.text, 'html.parser')
    count = soup.find_all('div', class_ = className)
    return len(count)
    
link = 'https://www.meubuzu.com.br/linhas?page='
i=1
totalPag = 2
linhasPorPag = 20
linhasNome = []
percursoNome = []
classNameIn = 'col-xs-12 line-item-name'

while(i < totalPag):
    pageOut = requests.get(link + str(i))
    k = 0
    if(pageOut.status_code == 200):
        soupOut = BeautifulSoup(pageOut.text, 'html.parser')
        while(k < linhasPorPag):
            temp = soup.find_all('span', class_ = 'visible-xs')[k].get_text()
            linhasNome.append(remover_acentos(temp))
            print(linhasNome)
            strLinkIn = str(temp.find('a')['href'])
            print(strLinkIn)
            pageIn = requests.get(strLinkIn)
            if(pageIn.status_code == 200):
                soupIn = BeautifulSoup(pageIn.text, 'html.parser')
                j = countDivClass(pageIn, classNameIn)
                m = 0
                while(m < j):
                    tempIn = soupIn.find_all(class_ = 'col-xs-12 line-item-name')[m].get_text()
                    percursoNome.append([remover_acentos(temp), remover_acentos(tempIn)])
                    m+=1
            k+=1
            if(i == totalPag):
                k = 20
                break
    i+=1


dfLinhasSite.to_excel('linhasSite.xls')
dfData = pd.read_excel('/home/dagoberto/Documentos/TRABALHO/regioes.xlsx', 'Plan1')
df = pd.DataFrame(dfData)
#dfData['Bairro'].head()

#pegando os codigos linhas
linhas = []
bairros = []
hifen = []
barra = []
i = 0
while(i < len(forecast_itens)):
    forecast_itens[i] = forecast_itens[i].replace(')', '-')
    forecast_itens[i] = forecast_itens[i].replace('(', '')
    forecast_itens[i] = forecast_itens[i].upper()
    #print(forecast_itens[i].find('-00'))
    if(forecast_itens[i].find('-00') == 4):
        linhas.append(forecast_itens[i][0:4])
    else:
        linhas.append(forecast_itens[i][0:7])
        hifen.append(forecast_itens[i].split('-'))
    i+=1


#contando a quantidade de linhas por bairro
i=0
#dfData['qtdLinhas'] = 0
listQtdLinhas = []
while(i < 169):
    j=0
    listQtdLinhas.append(j)
    while(j < len(forecast_itens)):
        if(re.search(dfData.loc[i, 'Bairro'], forecast_itens[j]) != None):
            listQtdLinhas[i] = listQtdLinhas[i]+1
        j+=1
    i+=1

dfData['qtdLinhas'] = listQtdLinhas

dfData.to_excel('df_linhas.xls')
