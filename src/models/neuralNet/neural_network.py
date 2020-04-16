import pandas as pd
import numpy as np

def TransformDataToX(df, date): 
    
    def dummie_and_drop(df, name):
        # Creates a dummy variable, concatenates it and finally drops the original categorical variable
        dummies = pd.get_dummies(df[name]).rename(columns = lambda x: name + '_' + str(x))
        df = pd.concat([df, dummies], axis = 1)
        df.drop(columns = [name], inplace=True, axis=1)

        return df
   
    x = df[['temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'precipitation', 'sky_level',
            'daytype', 'Day Name', 'Month', 'Hour', 'Quarter', 'Fare Last Month', 'Tips Last Month', 'Trips Last Hour',
            'Trips Last Week (Same Hour)', 'Trips 2 Weeks Ago (Same Hour)', 'trip_start_timestamp']]

    categorical_variables = ['sky_level', 'daytype', 'Day Name', 'Month', 'Hour', 'Quarter']
    for var in categorical_variables:
        x = dummie_and_drop(x, name = var)

    x = x[x['trip_start_timestamp'] == date]
    x = x.groupby('trip_start_timestamp').mean()
    x = x.to_numpy()

    return x

def TransformYToResult(Y):
    Y = Y.clip(min = 0)
    result = np.round(Y).astype('int')

    return result 