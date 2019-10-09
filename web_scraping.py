#!/usr/bin/env python
# coding: utf-8

# In[81]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unicodedata import normalize


# <b>Coletando as linhas com código e bairros de origem e destino de toda a cidade através do site meubuzu</b>

# In[86]:


#removendo acentuação
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


# In[93]:


link = 'https://www.meubuzu.com.br/linhas?page='
i=1
totalPag = 25
linhasPorPag = 20
forecast_itens = []
while(i <= totalPag):
    page = requests.get(link+ str(i))
    k=0
    if(page.status_code):
        soup = BeautifulSoup(page.content, 'html.parser')
        while(k < linhasPorPag):
            temp = soup.find_all('span', class_ = 'visible-xs')[k].get_text()
            forecast_itens.append(remover_acentos(temp))
            k+=1
            if(i == totalPag):
                k = 20
                break
    i+=1


# In[94]:


dfData = pd.read_excel('/home/dagoberto/Documentos/TRABALHO/regioes.xlsx', 'Plan1')
df = pd.DataFrame(dfData)
#dfData['Bairro'].head()


# In[95]:


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

#dar tratamento, aos dados, separar códigos e bairros e relaciona-los
# In[ ]:





# <b>Fazer nova coleta no site meubuzu coletando todos os percursos por linha</b>

# In[96]:


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
    


# In[97]:


dfData['qtdLinhas'] = listQtdLinhas


# In[98]:


dfData


# In[ ]:




