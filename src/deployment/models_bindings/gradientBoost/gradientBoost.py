#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np

def TransformDataToX(df, date): 
    
    def dummie_and_drop(df, name):
        # Creates a dummy variable, concatenates it and finally drops the original categorical variable
        dummies = pd.get_dummies(df[name]).rename(columns = lambda x: name + '_' + str(x))
        dummies = dummies.drop(dummies.columns[-1], axis = 1)
        df = pd.concat([df, dummies], axis = 1)
        df.drop(columns = [name], inplace=True, axis=1)

        return df
    
    def convert_to_categorical(df, categorical_variables, categories, need_pickup = True):
        """ 
        The dataframe's selected variables are converted to categorical, and each variable's categories are also specified.
        It is also specified if the "pickup community area" has to be converted into categorical or no. If it is not 
        converted into categorical it is because it's not going to be used in the model.            
        """
        
        if need_pickup:
            begin = 0
        else:
            df.drop(columns = ['pickup_community_area'], inplace = True, axis = 1)
            begin = 1
        
        for i in range(begin, len(categorical_variables)):
            df[categorical_variables[i]] = df[categorical_variables[i]].astype('category').cat.set_categories(categories[i])
        return df
    
    
    need_pickup = True
    
    x = df[['pickup_community_area' ,'temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'precipitation_cat', 
                'sky_level', 'daytype', 'Day Name', 'Month', 'Hour', 'Fare Last Month', 'Trips Last Hour',
                'Trips Last Week (Same Hour)', 'Trips 2 Weeks Ago (Same Hour)', 'Year', 'trip_start_timestamp']]

    categorical_variables = ['pickup_community_area', 'daytype', 'sky_level', 'Day Name', 'Month','Hour', 'Year']
    categories = [[*(range(1,78))], ['U', 'W', 'A'], ['OVC', 'BKN', 'SCT', 'FEW', 'CLR', 'VV '], 
                      ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                      [*(range(1,13))], [*(range(0, 24))], [2017, 2018, 2019]]
    
    
    x = convert_to_categorical(x, categorical_variables, categories, need_pickup = need_pickup)
    
    
    float32=['temperature','relative_humidity','wind_direction','wind_speed','Fare Last Month', 'Trips Last Hour',
                'Trips Last Week (Same Hour)', 'Trips 2 Weeks Ago (Same Hour)']
        
    x[float32]=x[float32].astype('float32')
    # Make dummy variables with the categorical ones
    if need_pickup:
        begin = 0
    else:
        begin = 1
    for i in range(begin, len(categorical_variables)):
        x = dummie_and_drop(x, name = categorical_variables[i])
        
    x = x[x['trip_start_timestamp'].str.contains(date)]
    x.drop(columns=['trip_start_timestamp'],axis=1,inplace=True)
    


    x = x.to_numpy()

    return x


# In[54]:


def TransformYToResult(Y):
    Y = Y.clip(min = 0)/2
    result = np.round(Y).astype('int')

    return result 


# In[ ]:




