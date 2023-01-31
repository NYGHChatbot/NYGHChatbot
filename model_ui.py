import nltk
import random
import json
import pickle
import numpy as np
import time

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

model = load_model('model.h5')
intents = json.loads(open('intents.json',encoding="utf8").read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
totalResponseTime = 0
numberOfResponses = 0

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    KeyWords = ["covid-19", "covid19", "coronavirus", "corona virus", "covid", "corona", "mask", "masks",
                "bivalent", "antiviral treatments", "antiviral treatment", "paxlovid",
                "hi", "hey", "hello", "greetings", "help", "what can you do", "what you can do"
                "bye", "see you later", "goodbye", "have a good day", "have a nice day", "have a good one",
                "see you soon", "have a good night", "thanks", "thank you", "Awsome",
                "flu", "flushot", "influenza", "monkeypox", "monkey pox"]
    helper = set()
    lowered_case = msg.lower()
    for KeyWord in KeyWords:
      helper.add(lowered_case.find(KeyWord))
    
    # for non-related questions
    if len(helper) == 1:
      return "Sorry, I don't understand your question. I can only answer questions regarding Monkeypox, Influenza (flu), and Covid-19. If you have any questions other than areas mentioned, you can contact NYGH's Pharmacy at (416)756-6666 or email them through NYGHPharmacy@nygh.on.ca"
 
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def startTimer():
    start = time.time()
    return start

def endTimer():
    end = time.time()
    return end

def calculateAverageTime(start, end):
    global totalResponseTime
    global numberOfResponses

    difference = end - start
    numberOfResponses = numberOfResponses + 1
    totalResponseTime = round(totalResponseTime + difference, 5)
    averageResponseTime = totalResponseTime / numberOfResponses

    print("New Average Response Time: ", averageResponseTime * 1000, "ms")
