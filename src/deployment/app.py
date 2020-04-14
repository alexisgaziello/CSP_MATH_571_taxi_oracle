import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import importlib.util, os


# Get current path from where script is executed
if os.name == 'nt':
    sep = '\\'
elif os.name == 'posix':
    sep = '/'
else:
    print(f'What is this OS? {os.name}')

path = os.getcwd()
pathToSrc =  path[:-len(f'deployment')]
pathToGDrive =  path[:-len(f'Code{sep}src{sep}project_CSP_MATH_571')]
path_datasets = pathToGDrive + f'DataSets{sep}trips{sep}'

#MapGenerator Lib
path_maps = pathToSrc + f'{sep}mapGeneration{sep}mapGeneration.py'
spec = importlib.util.spec_from_file_location("mapGeneration", path_maps)
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    # Get values from form.
    # for  x in request.form.values:
        
    # int_features = [x for x in request.form.values()]

    # Transform to array X
    # final_features = [np.array(int_features)]

    # Predict
    # prediction = model.predict(final_features)
    prediction = np.random.randint(1,200,77)
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