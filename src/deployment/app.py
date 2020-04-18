import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import importlib.util, os, sys
import pandas as pd
import joblib

# Get current path from where script is executed
if os.name == 'nt':
    sep = '\\'
elif os.name == 'posix':
    sep = '/'
else:
    print(f'What is this OS? {os.name}')

# Paths
path = os.path.dirname(sys.argv[0])
pathToSrc =  path[:path.find('src')+3]
pathToGDrive =  path[:path.find('Code')]
pathToDatasets = pathToGDrive + f'DataSets{sep}'

# MapGenerator Lib
path_maps = pathToSrc + f'{sep}mapGeneration{sep}mapGeneration.py'
spec = importlib.util.spec_from_file_location("mapGeneration", path_maps)
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)
communities = mp.loadCommunities()

# Dataset
pathToDataSet = pathToDatasets + 'dataset_test.csv'
df = pd.read_csv(pathToDataSet)
#df = df.drop(columns=['Unnamed: 0'],axis=1)

# Models

# Linear Regression

# RandomForest 
# model_randomForest = joblib.load(path_datasets+"/model/randomforest.pkl")

# path_to_model = pathToSrc + f'{sep}models{sep}/randomForest/randomForest.py'
# spec = importlib.util.spec_from_file_location("randomForest", path_to_model)
# randomForest = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(randomForest)

# Neural Net
path_to_model = pathToSrc + f'{sep}models{sep}neuralNet{sep}neural_network.py'
spec = importlib.util.spec_from_file_location("neuralNet", path_to_model)
neuralNet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neuralNet)

# Ensambling

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():


    # Get values from form.
    # date = "2019-12-16 16:00:00"
    # Get date

    day = request.form.get('day')
    hour = request.form.get('hour')
    seconds = '00'
    date = day + ' ' + hour + ':' + seconds

    # Real Y (values)
    real = df.loc[df.trip_start_timestamp == "2019-11-01 00:00:00"]['Trips']
    real_img = mp.mapGenerator(real, communities=communities, saveByte=True) 
        
    # Transform to array X
    # X = randomForest.TransformDataToX(df, date)


    # Predict
    #Y = model_randomForest.predict(X)
    #prediction = np.random.randint(1,200,77)
    # Create map

    #prediction = randomForest.TransformYToResult(Y)

    # Create map
    #result = mp.mapGenerator(prediction, communities=communities, saveByte=True)    

    # Neural Net
    # X = neuralNet.TransformDataToX(df, date)
    # Y = model_neural_network.predict(X)
    # prediction = neuralNet.TransformYToResult(Y)
    # neuralNet_img = mp.mapGenerator(prediction, communities=communities, saveByte=True)

    result = real_img
    regression_img=result
    randomForest_img = result
    ensambling_img = result
    neuralNet_img = result

    return render_template('predict.html'
        , real=real_img
        , regression=regression_img
        , randomForest = randomForest_img
        , ensambling = ensambling_img
        , neuralNet = neuralNet_img)


# For requests and JSON 
@app.route('/results',methods=['POST'])
def results():

    print("NOT IMPLEMENTED")
    return
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)