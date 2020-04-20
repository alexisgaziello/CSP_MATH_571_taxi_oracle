import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import importlib.util, os, sys
import pandas as pd
import joblib
from keras.models import model_from_json

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
print("\nLoading Datasets...")
pathToDataSet = pathToDatasets + 'dataset_test.csv'
df = pd.read_csv(pathToDataSet)

minDate = df.iloc[0,].trip_start_timestamp[:10]
maxDate = df.iloc[-1,].trip_start_timestamp[:10]
defaultDate = df.iloc[int(len(df)/2),].trip_start_timestamp[:10]

#df = df.drop(columns=['Unnamed: 0'],axis=1)

# Models

# Random Forest
print("\nLoading Random Forest...")

model_randomForest = joblib.load(pathToDatasets+"/model/randomForest.pkl")

path_to_model = pathToSrc + f'{sep}models{sep}/randomForest/randomForest.py'
spec = importlib.util.spec_from_file_location("randomForest", path_to_model)
randomForest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(randomForest)
# Regression
print("\nLoading Regression...")

# Gradient BR
print("\nLoading Gradient BR...")


# Neural Net
print("\nLoading Neural Net...")
# Model
pathNeuralNet = pathToSrc + f'{sep}models{sep}neuralNet{sep}'

# load json and create model
json_file = open(pathNeuralNet + 'model_neural_network.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model_neural_network = model_from_json(loaded_model_json)
# load weights into new model
model_neural_network.load_weights(pathNeuralNet + "model_neural_network.h5")

# Bindings
spec = importlib.util.spec_from_file_location("neuralNet", pathNeuralNet+'neural_network.py')
neuralNet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neuralNet)


# Flask deployment

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', minDate=minDate, maxDate=maxDate, defaultDate=defaultDate)

@app.route('/predict',methods=['POST'])
def predict():


    # Get values from form.
    # date = "2019-12-16 16:00:00"
    # Get date

    day = request.form.get('day')
    hour = request.form.get('hour')
    seconds = '00'
    date = day + ' ' + hour + ':' + seconds
    
    print(f"\nPredicting for :{date}")

    # Transform to array X
    # X = randomForest.TransformDataToX(df, date)

    # Predict
    #prediction = randomForest.TransformYToResult(Y)

    # Create map
    #result = mp.mapGenerator(prediction, communities=communities, saveByte=True)    

    # Real Y (values)
    real = df.loc[df.trip_start_timestamp == "2019-11-01 00:00:00"]['Trips']
    real_img = mp.mapGenerator(real, communities=communities, saveByte=True) 

    # Random Forest
    X = randomForest.TransformDataToX(df, date)
    Y = model_randomForest.predict(X)
    prediction = randomForest.TransformYToResult(Y)
    randomForest_img = mp.mapGenerator(prediction, communities=communities, saveByte=True)
    
    # Regression

    # Gradient Boosting

    # Neural Net
    X = neuralNet.TransformDataToX(df, date)
    Y = model_neural_network.predict(X)
    prediction = neuralNet.TransformYToResult(Y)
    neuralNet_img = mp.mapGenerator(prediction, communities=communities, saveByte=True)


    # Random values
    # np.random.randint(1,200,77)
    result = real_img
    regression_img=result
    # randomForest_img = result
    gradientBoost_img = result
    # neuralNet_img = result

    return render_template('predict.html'
        , real=real_img
        , regression=regression_img
        , randomForest = randomForest_img
        , gradientBoost = gradientBoost_img
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