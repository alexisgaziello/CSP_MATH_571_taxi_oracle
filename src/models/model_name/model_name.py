import pickle # NO CHANGE

# To save model:
# Calculate it and then save it with:
# you don't have to call the following gunction here. call it in your script
pickle.dump(model, open('model_name.pkl','wb'))


import # necessary libraries to load the model for example import skleanr.whatever.

def model_name_Load(): # NO CHANGE
    # check you have the necessary libraries to use the model, if there is need for any
    # maybe call predict or something
    # after you can delete everything inside this function and just leave the pickle.load
    return pickle.load(open('model.pkl','rb')) # NO CHANGE

def model_name_TransformDataToX(data): # NO CHANGE
    #Perform calculations. Data is a row of the selected date.
    return X # NO CHANGE

def model_name_TransformYToResult(Y): # NO CHANGE
    # Perform neccesary transformations. Result  is an array of size 77 in which each item
    #  it's the value of taxi trips for each community in order 
    # (meaning first value is for community 1, second for community 2, etc) 
    # OR a dictionary with the key as the community
    #  and the value the predicted trips.

    return result # NO CHANGE