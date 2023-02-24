from flask import Flask, render_template, request, jsonify
from model_ui import chatbot_response, startTimer, endTimer, calculateAverageTime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('base.html')

@app.post("/predict")
def predict():
    start = startTimer()
    text = request.get_json().get("message")
    response, add_message = chatbot_response(text)
    message = {"answer": response, "add_message": add_message}
    end = endTimer()
    calculateAverageTime(start, end)
    return jsonify(message)

@app.post("/confirm")
def confirm():
    return jsonify("helllo")
