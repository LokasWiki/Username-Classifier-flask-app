import os
import configparser
from markupsafe import escape
from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)
home_path = os.path.expanduser("~")
__dir__ = os.path.dirname(__file__)

# Initialize the spam classifier outside of the Flask application
spam_classifier_generator = pipeline(model="lokas/spam-usernames-classifier")




# Read the API key from the config file
config_path = os.path.join(home_path, 'config.ini')
# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

api_key = config['API']['key']


@app.route('/')
def index():
    return {"status": "working"}


@app.route('/predict', methods=['POST'])
def predict_view():
    # Check if the API key is present in the request header
    api_key_header = request.headers.get('X-Api-Key')
    if api_key_header != api_key:
        return {"message": "Unauthorized"}, 401

    # Extract the list of usernames from the request body
    usernames = request.json.get('usernames', [])

    # Run the spam classifier on each username and return the results
    predictions = spam_classifier_generator(usernames)
    results = [{"username": username, "prediction": prediction} for username, prediction in zip(usernames, predictions)]
    return {"results": results}


if __name__ == "main":
    app.run()
