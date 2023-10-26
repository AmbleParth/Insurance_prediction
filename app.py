#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

#default page of our web-app
@app.route('/')
def home():
    return render_template('index.html')

#To use the predict button in our web-app
# Modify your /predict route as follows:
# Modify your /predict route as follows:
def map_region_to_numeric(region):
    region_mapping = {
        'southeast': 0,
        'southwest': 1,
        'northeast': 2,
        'northwest': 3
    }
    return region_mapping.get(region, 0)  # Default to 0 if region is not recognized
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [request.form['Age'], request.form['BMI'], request.form['Children']]
    sex = request.form['Sex']
    smoker = request.form['Smoker']
    region = request.form['Region']

    # Encoding categorical variables
    sex_encoded = 0 if sex == 'male' else 1
    smoker_encoded = 0 if smoker == 'yes' else 1

    # Map 'region' to a numerical value (or one-hot encode it if there are multiple categories)
    region_encoded = map_region_to_numeric(region)

    # Create a list of features for prediction
    features = [float(int_features[0]), sex_encoded, float(int_features[1]), smoker_encoded, float(int_features[2]), region_encoded]

    final_features = [np.array(features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Price of insurance is: ${}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)