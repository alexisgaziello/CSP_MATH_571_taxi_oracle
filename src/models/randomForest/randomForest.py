import pickle # NO CHANGE

# To save model:
# Calculate it and then save it with:
# you don't have to call the following gunction here. call it in your script


import # necessary libraries to load the model for example import skleanr.whatever.

def model_name_TransformDataToX(row): # NO CHANGE
    row['trip_start_timestamp'] = pd.to_datetime(row['trip_start_timestamp'])

    #Perform calculations. Data is a row of the selected date.
    return X # NO CHANGE

def model_name_TransformYToResult(Y):

    return Y