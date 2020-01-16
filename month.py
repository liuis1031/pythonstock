#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from io import StringIO
import time
def monthly_report(year, month):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    df = df.set_index(['公司代號'])
    
    # 偽停頓
    time.sleep(5)

    return df


# In[40]:


import datetime

now = datetime.datetime.now()

year = now.year - 1911
month = now.month - 1

if month == 0:
    month = 12
    year -= 1
else:
    year = now.year - 1911
    month == now.month - 1

print(year, month)

df = monthly_report(year, month)


# In[36]:


df.loc[['5283','6669','2227','2891','2888','9927']]


# In[4]:


df.describe()


# In[5]:


import datetime
import pandas as pd
import time

data = {}
n_days = 12
now = datetime.datetime.now()

year = now.year
month = now.month

while len(data) < n_days:
    
    print('parsing', year, month)
    
    # 使用 crawPrice 爬資料
    try:
        data['%d-%d-01'%(year, month)] = monthly_report(year, month)
    except Exception as e:
        print('get 404, please check if the revenues are not revealed')
    
    # 減一個月
    month -= 1
    if month == 0:
        month = 12
        year -= 1

    time.sleep(10)


# In[6]:


data['2019-12-01']


# In[7]:


for k in data.keys():
    data[k].index = data[k]['公司名稱']
    
df = pd.DataFrame({k:df['當月營收'] for k, df in data.items()}).transpose()
df.index = pd.to_datetime(df.index)
df = df.sort_index()


# In[8]:


df.head()


# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt

df['禾聯碩'].plot()


# In[14]:


x = pd.to_datetime(df.index)
y = [0,0,0,0,0,0,0,0,0,0,0,0]
plt.plot(x, y, linewidth=1,color='gray')
plt.ylabel("Y")
plt.xlabel("X") 
((df['禾聯碩']/df['禾聯碩'].shift() - 1) *100).plot()
plt.show()


# In[11]:


df['緯穎'].plot()


# In[13]:


x = pd.to_datetime(df.index)
y = [0,0,0,0,0,0,0,0,0,0,0,0]
plt.plot(x, y, linewidth=1,color='gray')
plt.ylabel("Y")
plt.xlabel("X") 
((df['緯穎']/df['緯穎'].shift() - 1) *100).plot()
plt.show()


# In[ ]:




