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
    
    
    need_pickup = False
    
    x = df[['pickup_community_area' ,'temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'precipitation_cat', 
                'sky_level', 'daytype', 'Day Name', 'Month', 'Hour', 'Fare Last Month', 'Trips Last Hour',
                'Trips Last Week (Same Hour)', 'Trips 2 Weeks Ago (Same Hour)', 'Quarter', 'Year', 'trip_start_timestamp']]

    categorical_variables = ['pickup_community_area', 'daytype', 'sky_level', 'Day Name', 'Month','Hour', 'Year']
    categories = [[*(range(1,78))], ['U', 'W', 'A'], ['OVC', 'BKN', 'SCT', 'FEW', 'CLR', 'VV '], 
                      ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                      [*(range(1,13))], [*(range(0, 24))], [2017, 2018, 2019]]
    
    
    x = convert_to_categorical(x, categorical_variables, categories, need_pickup = need_pickup)
    
    # Make dummy variables with the categorical ones
    if need_pickup:
        begin = 0
    else:
        begin = 1
    for i in range(begin, len(categorical_variables)):
        x = dummie_and_drop(x, name = categorical_variables[i])
    

    x = x[x['trip_start_timestamp'] == date]
    x = x.groupby('trip_start_timestamp').mean()
    x = x.to_numpy()

    return x

def TransformYToResult(Y):
    Y = Y.clip(min = 0)/2
    result = np.round(Y).astype('int')

    return result 






# def load_data(date):
    
#     def dummie_and_drop(df, name):
#         # Creates a dummy variable, concatenates it and finally drops the original categorical variable.
#         # In order not to have redundant variables, one of the dummy variables is dropped too
#         dummies = pd.get_dummies(df[name]).rename(columns = lambda x: name + '_' + str(x))
#         dummies = dummies.drop(dummies.columns[-1], axis = 1)
#         df = pd.concat([df, dummies], axis = 1)
#         df.drop(columns = [name], inplace=True, axis=1)

#         return df
    
#     def convert_to_categorical(df, categorical_variables, categories, need_pickup = True):
#         """ 
#         The dataframe's selected variables are converted to categorical, and each variable's categories are also specified.
#         It is also specified if the "pickup community area" has to be converted into categorical or no. If it is not 
#         converted into categorical it is because it's not going to be used in the model.            
#         """
        
#         if need_pickup:
#             begin = 0
#         else:
#             df.drop(columns = ['pickup_community_area'], inplace = True, axis = 1)
#             begin = 1
        
#         for i in range(begin, len(categorical_variables)):
#             df[categorical_variables[i]] = df[categorical_variables[i]].astype('category').cat.set_categories(categories[i])
#         return df
    
    
#     def load(name, date, need_pickup = False, drop_correlated = False):
    
#         # This parameter has to be set to True if the "pickup_community_area" variable is needed in the model
        

#         # Load needed dataset and choose the useful columns
#         df = pd.read_csv(name) #'dataset_train.csv')
#         df = df[df['trip_start_timestamp'].str.slice(start = 0, stop = 13) == date]
#         x = df[['pickup_community_area' ,'temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'precipitation_cat', 
#                 'sky_level', 'daytype', 'Day Name', 'Month', 'Hour', 'Fare Last Month', 'Trips Last Hour',
#                 'Trips Last Week (Same Hour)', 'Trips 2 Weeks Ago (Same Hour)', 'Quarter', 'Year', 'trip_start_timestamp']]

#         # Convert the categorical variables
#         categorical_variables = ['pickup_community_area', 'daytype', 'sky_level', 'Day Name', 'Month','Hour', 'Year']
#         categories = [[*(range(1,78))], ['U', 'W', 'A'], ['OVC', 'BKN', 'SCT', 'FEW', 'CLR', 'VV '], 
#                       ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
#                       [*(range(1,13))], [*(range(0, 24))], ['2017', '2018', '2019']]

#         x = convert_to_categorical(x, categorical_variables, categories, need_pickup = need_pickup)

        
#         # Make dummy variables with the categorical ones
#         if need_pickup:
#             begin = 0
#         else:
#             begin = 1
#         for i in range(begin, len(categorical_variables)):
#             x = dummie_and_drop(x, name = categorical_variables[i])
        
        
        
#         y = df['Trips'].to_numpy()

#         if need_pickup == False:
#             # If we don't need the pickup, it means this is Neural Network case. Therefore we have to modify Y, in order
#             # to have "n_areas" outputs per input (because there are "n_areas" regressions per input)
#             x = x.groupby(by = 'trip_start_timestamp').mean()
#             n_areas = 77
#             y = np.reshape(y, [-1, n_areas]) # If 
#         else:
#             x.drop(columns = ['trip_start_timestamp'], inplace = True, axis = 1)
        
#         if drop_correlated:
#             x.drop(columns = ['Trips Last Week (Same Hour)'], inplace = True, axis = 1)
#             x.drop(columns = ['Trips 2 Weeks Ago (Same Hour)'], inplace = True, axis = 1)

#         x = x.to_numpy()
        
#         return (x,y)   
    

#     need_pickup = False 
#     drop_correlated = False
    

#     name_test = 'dataset_test.csv'
#     x_test, y_test = load(name_test, date, need_pickup, drop_correlated)
    
    
#     return (x_test, y_test)



