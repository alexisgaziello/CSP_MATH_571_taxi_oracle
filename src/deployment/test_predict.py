#!/usr/bin/env python
# coding: utf-8

# In[506]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib 
import pickle


# In[507]:



cd "C:/Users/Iconsense/abhishek/taxi"


# In[508]:


df = pd.read_csv('dataset_final.csv')
df.drop(columns=['trip_start_timestamp.1','pickup_community_area.1','Trips'],inplace=True)


# In[509]:


def model_name_Load(): # NO CHANGE
    # check you have the necessary libraries to use the model, if there is need for any
    # maybe call predict or something
    # after you can delete everything inside this function and just leave the pickle.load
    # Load the model from the file 
    rf = joblib.load('filename.pkl')  
    return rf


# In[510]:


rf=model_name_Load()


# In[ ]:





# In[517]:


dftest = pd.read_csv('prediction.csv')

dftest.drop(columns=['trip_start_timestamp.1','pickup_community_area.1','Trips'],inplace=True)


# In[512]:


def transformX(df,dftest,datetime):

    dftest = dftest[dftest['trip_start_timestamp'].str.contains(datetime)] 
    dftest['trip_start_timestamp'] = pd.to_datetime(dftest['trip_start_timestamp'])
    
    
    df.append(dftest)
    
    df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

    df['weekofyear']=df['trip_start_timestamp'].dt.weekofyear

    df['day'] = df['trip_start_timestamp'].dt.day

    df['year'] = df['trip_start_timestamp'].dt.year

    df.drop(columns=['trip_start_timestamp'],inplace=True)

    categorical_cols = ['pickup_community_area','day',
                'weekofyear','Quarter','Hour','Month','Day Name','sky_level','daytype']


    numerical_cols =['Trips','year' 'temperature', 'relative_humidity','wind_direction','wind_speed','precipitation','Fare Last Month',
                'Tips Last Month','Trips Last Hour','Trips Last Week (Same Hour)','Trips 2 Weeks Ago (Same Hour)']

    df[categorical_cols] = df[categorical_cols].apply(pd.Categorical) 

    df['sky_level']=df['sky_level'].map({'CLR':0, 'FEW':1, 'SCT':2, 'BKN':3, 'OVC': 4})

    df.fillna(df.median(),inplace=True)

    df=pd.get_dummies(df, columns=['pickup_community_area','day','weekofyear','Quarter','Hour','Month','Day Name','daytype'],drop_first=True)
    df=df.iloc[1920072:]
    float64=['sky_level','Fare Last Month','Tips Last Month','temperature','relative_humidity','wind_direction','wind_speed','precipitation']

    df[float64]=df[float64].astype('float32')
    

    
    return df


# In[513]:


x=transformX(df,dftest,datetime)


# In[514]:


def model_name_TransformYToResult(x): # NO CHANGE
    # Perform neccesary transformations. Result  is an array of size 77 in which each item
    #  it's the value of taxi trips for each community in order 
    # (meaning first value is for community 1, second for community 2, etc) 
    # OR a dictionary with the key as the community
    #  and the value the predicted trips.
    result=rf.predict(x)
    result=result.astype(int)
    return result


# In[515]:


result=model_name_TransformYToResult(x)


# In[516]:


print(result)


# In[ ]:




