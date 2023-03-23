import os

from markupsafe import escape
from transformers import pipeline
import pytorch

from flask import Flask, render_template, request, url_for, abort, request, url_for, flash, redirect

app = Flask(__name__)

__dir__ = os.path.dirname(__file__)

spam_classifier_generator = pipeline(model="lokas/spam-usernames-classifier")




@app.route('/')
def index():
    return {
        "status": "working"
    }


# Define a route for making predictions
# todo:add api key
@app.route('/predict', methods=['POST'])
def predict_view():
    username = request.form['username']
    prediction = spam_classifier_generator([username])
    return {
        "username": username,
        "prediction": prediction,
    }

if __name__ == "main":
    app.run()