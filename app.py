import os
import configparser
from markupsafe import escape
from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)
home_path = os.path.expanduser("~")
__dir__ = os.path.dirname(__file__)

# Read the API key from the config file
config_path = os.path.join(home_path, 'config.ini')
# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

api_key = config['API']['key']

# Initialize the spam classifier outside of the Flask application
spam_classifier_generator = None

@app.before_first_request
def load_model():
    # Load the spam classifier outside of the Flask application
    global spam_classifier_generator
    spam_classifier_generator = pipeline(model="lokas/spam-usernames-classifier")

@app.route('/')
def index():
    return {"status": "working"}


@app.route('/predict', methods=['POST'])
def predict_view():

    # Check if the API key is present in the request header
    api_key_header = request.headers.get('X-Api-Key')
    if api_key_header != api_key:
        return {"message": "Unauthorized"}, 401

    # Parse the request data as JSON
    req_data = request.get_json()

    # Check if the request data is None or empty
    if not req_data:
        return {"message": "Request data is empty or not in JSON format"}, 400

    # Extract the list of usernames from the request body
    usernames = req_data['usernames'] if 'usernames' in req_data else []

    # Check if the list of usernames is empty
    if not usernames:
        return {"message": "Empty list of usernames"}, 400

    # Run the spam classifier on each username and return the results
    predictions = spam_classifier_generator(usernames)
    results = [{"username": username, "prediction": prediction} for username, prediction in zip(usernames, predictions)]
    return {"results": results}


if __name__ == "__main__":
    app.run()
