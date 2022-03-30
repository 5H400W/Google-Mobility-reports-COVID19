# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:28:17 2022

@author: Prashant Dwivedi


"""

import matplotlib.pyplot as plt
from pylab import rcParams

gmd = pd.read_csv(r"C:\Users\\Global_Mobility_Report.csv")


# In[2]:


gmd.head()


# In[3]:


NY_data = gmd.loc[(gmd['country_region']=='United States') & (gmd['sub_region_1'] == 'New York') ]


# In[4]:


NY_data.head()


#  set(list(NY_data['sub_region_2']))

# In[5]:


M_data=NY_data.loc[NY_data['sub_region_2']=='New York County']
M_data.head()


# # Descritptive Analysis

# In[6]:


M_data['retail_and_recreation_percent_change_from_baseline'].max()


# In[7]:


M_data['date'].loc[M_data['retail_and_recreation_percent_change_from_baseline']==6.0]


# In[8]:


M_data['retail_and_recreation_percent_change_from_baseline'].min()


# In[9]:


M_data['date'].loc[M_data['retail_and_recreation_percent_change_from_baseline']==-89.0]


# In[10]:


M_data['retail_and_recreation_percent_change_from_baseline'].mean()


# # PLOT THE MOBILITY TREND

# In[11]:


M_data['date']=pd.to_datetime(M_data['date'])


# In[12]:


M_data = M_data.set_index('date')


# In[13]:


M_data.head()


# In[14]:


M_data['retail_and_recreation_percent_change_from_baseline'].plot()
plt.show()


# In[20]:


M_data['retail_and_recreation_percent_change_from_baseline'].plot(ls='--',color='blue',label='Retail')
M_data['grocery_and_pharmacy_percent_change_from_baseline'].plot(ls='--',color='orange',label='Grocery')
M_data['parks_percent_change_from_baseline'].plot(marker='X',color='purple',label='Park')
M_data['transit_stations_percent_change_from_baseline'].plot(ls='--',color='red',label='transit')
M_data['workplaces_percent_change_from_baseline'].plot(ls='--',color='yellow',label='Workplace')
M_data['residential_percent_change_from_baseline'].plot(ls='--',color='cyan',label='Residental')

plt.title('Mobility',fontdict=None,loc='center',pad=None)

plt.legend()

plt.show()
from pylab import rcParams
rcParams['figure.figsize'] = 100, 50

