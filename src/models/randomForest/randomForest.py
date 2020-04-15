import numpy as np

def TransformDataToX(df, date): # NO CHANGE    
    
    df = df[df['trip_start_timestamp'].str.contains(date)]
    df.drop(columns=['trip_start_timestamp'],axis=1,inplace=True)
    
    X=np.array(df)
    
    #Perform calculations. Data is a row of the selected date.
    return X # NO CHANGE

def TransformYToResult(Y):

    result = Y.astype(int)
    result = result.tolist()

    return result