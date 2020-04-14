#!/usr/bin/env python
# coding: utf-8

# In[56]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib 
import pickle


 


# In[57]:



cd "C:/Users/Iconsense/abhishek/taxi"


# In[58]:


rf = joblib.load('filename.pkl') 


# In[59]:


df = pd.read_csv('dataset_final.csv')
y=df["Trips"]
df.drop(columns=['trip_start_timestamp.1','pickup_community_area.1','Trips'],inplace=True)


# In[60]:


df.columns


# In[ ]:





# In[61]:


def transformX(df,trip_start_timestamp,temperature,relative_humidity,wind_direction,wind_speed,precipitation,daytype,sky_level,Day_Name,Month,Hour,Quarter,Fare_Last_Month,Tips_Last_Month,Trips_Last_Hour,Trips_Last_Week,Trips_2_Weeks_Ago):
    
    
    row=[]
    for i in range(77):
        row.append([ trip_start_timestamp,i,temperature,relative_humidity,wind_direction,wind_speed,precipitation,daytype,sky_level,Day_Name,Month,Hour,Quarter,Fare_Last_Month,Tips_Last_Month,Trips_Last_Hour,Trips_Last_Week,Trips_2_Weeks_Ago])

    df2 = pd.DataFrame(row, columns = df.columns) 

    df.append(df2)

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
    df=df.iloc[:77]
    float64=['sky_level','Fare Last Month','Tips Last Month','temperature','relative_humidity','wind_direction','wind_speed','precipitation']

    df[float64]=df[float64].astype('float32')
    
    
    
    dfx = np.array(df)
    
    return dfx

    
 
        
    
        
        
        


# In[62]:


x=transformX(df,"2017-01-16 00:00:00",30.4,50,220,30,2,'A','OVC','Friday',1,0,1,0.0,0.0,0,0,0)


# In[63]:


predict=rf.predict(x)
predict.astype(int)


# In[ ]:




