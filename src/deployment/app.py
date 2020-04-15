import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import importlib.util, os
import pandas as pd
import joblib

# Get current path from where script is executed
if os.name == 'nt':
    sep = '\\'
elif os.name == 'posix':
    sep = '/'
else:
    print(f'What is this OS? {os.name}')

path = os.getcwd()
pathToSrc =  path[:path.find('src')+3]
pathToGDrive =  path[:path.find('Code')]
path_datasets = pathToGDrive + f'DataSets{sep}'

pathToDataSet = pathToGDrive + f'DataSets{sep}' + 'dataset_final.csv'
df = pd.read_csv(pathToDataSet)

# Models

#pickle.load(open('model.pkl','rb')) 

# MapGenerator Lib
path_maps = pathToSrc + f'{sep}mapGeneration{sep}mapGeneration.py'
spec = importlib.util.spec_from_file_location("mapGeneration", path_maps)
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

# RandomForest 
model_randomForest = joblib.load(path_datasets+"/model/randomforest.pkl")

path_to_model = pathToSrc + f'{sep}models{sep}/randomForest/randomForest.py'
spec = importlib.util.spec_from_file_location("randomForest", path_to_model)
randomForest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(randomForest)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():


    # Get values from form.
    date = "2017-01-16 00:00:00"#getDate from request.form.values:
    row = df[df['trip_start_timestamp'] == date].iloc[0,]
        
    # Transform to array X
    X = randomForest.TransformDataToX(row)


    # Predict
    Y = model_randomForest.predict(X)
    #prediction = np.random.randint(1,200,77)
    # Create map

    result = randomForest.TransformYToResult(Y)

    # Create map
    result = mp.mapGenerator(prediction, saveByte=True)    

    result = str(result)[2:-1]

    return render_template('predict.html', result=result)


# For requests and JSON 
@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)