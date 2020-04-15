#!/usr/bin/env python
# coding: utf-8

# In[28]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib 
import pickle


# In[29]:


cd "C:/Users/Iconsense/abhishek/taxi"


# In[30]:


rf = joblib.load('randomforest.pkl')  

df = pd.read_csv('pred.csv')


# In[31]:


df.drop(columns=['Unnamed: 0'],axis=1,inplace=True)


# In[32]:


df.shape


# In[33]:


def model_name_Load(): # NO CHANGE
    # check you have the necessary libraries to use the model, if there is need for any
    # maybe call predict or something
    # after you can delete everything inside this function and just leave the pickle.load
    # Load the model from the file 
    rf = joblib.load('filename.pkl')  
    return rf


# In[34]:


rf=model_name_Load()


# In[35]:


df.head()


# In[40]:


def transformX(date):

    dftest = dftest[dftest['trip_start_timestamp'].str.contains(date)] 
    
    df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])
    
    df.drop(columns=['trip_start_timestamp'],axis=1,inplace=True)
    
    x=np.array(df)
    
    return x


# In[41]:


def model_name_TransformYToResult(x): # NO CHANGE
    # Perform neccesary transformations. Result  is an array of size 77 in which each item
    #  it's the value of taxi trips for each community in order 
    # (meaning first value is for community 1, second for community 2, etc) 
    # OR a dictionary with the key as the community
    #  and the value the predicted trips.
    result=rf.predict(x)
    result=result.astype(int)
    return result


# In[ ]:


x=transformX(date)


# In[ ]:


result=model_name_TransformYToResult(x)


# In[ ]:


print(result)


# In[ ]:




