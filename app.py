from flask import Flask, render_template, request, jsonify
# from model_ui import chatbot_response


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('base.html')

# @app.post("/predict")
# def predict():
#     text = request.get_json().get("message")
#     response = chatbot_response(text)
#     message = {"answer": response}
#     return jsonify(message)
