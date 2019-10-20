import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unicodedata import normalize

#removendo acentuação
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
link = 'https://www.meubuzu.com.br/linhas?page=1'
page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')
temp = soup.find_all('div', class_ = 'col-sm-5 col-xs-10')[1]

print(temp.find('a')['href'])
print(temp.find('span').get_text())
strLinkIn = str(temp.find('a')['href'])
linkIn = strLinkIn
print('1')
pageIn =requests.get(linkIn)
print('2')
soupIn = BeautifulSoup(pageIn.content, 'html.parser')
print('3')
tempIn = soupIn.find_all('div', class_ = 'col-xs-12 line-item-name')
print('4')
print(tempIn)

link = 'https://www.meubuzu.com.br/linhas?page='
i=1
totalPag = 1
linhasPorPag = 20
forecast_itens = []
while(i <= totalPag):
    page = requests.get(link+ str(i))
    k=0
    if(page.status_code == 200): #melhorar os testes de acesso a página
        soup = BeautifulSoup(page.content, 'html.parser')
        while(k < linhasPorPag):
            temp = soup.find_all('span', class_ = 'visible-xs')[k].get_text()
            forecast_itens.append(remover_acentos(temp))
            k+=1
            if(i == totalPag):
                k = 20
                break
    i+=1

dfLinhasSite = pd.DataFrame(forecast_itens)


# In[103]:


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
