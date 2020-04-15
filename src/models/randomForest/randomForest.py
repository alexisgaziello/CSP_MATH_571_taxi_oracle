

def TransformDataToX(row): # NO CHANGE    
    row['trip_start_timestamp'] = pd.to_datetime(row['trip_start_timestamp'])
    
    row = row.drop(['trip_start_timestamp'])
    
    X=np.array(row)
    
    #Perform calculations. Data is a row of the selected date.
    return X # NO CHANGE

def TransformYToResult(Y):

    return Y