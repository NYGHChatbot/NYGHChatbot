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
    return result, tag

def chatbot_response(msg):
    add_message = False   
    KeyWords = ["covid-19", "covid19", "coronavirus", "corona virus", "covid", "corona", "mask", "masks",
                "bivalent", "antiviral treatments", "antiviral treatment", "paxlovid", "total cases in canada", 
                "statistics report", "statistics", "total cases", "sanitizer", "soap", "unauthorized vaccine",
                "hi", "hey", "hello", "greetings", "help", "what can you do", "what you can do",
                "bye", "see you later", "goodbye", "have a good day", "have a nice day", "have a good one",
                "see you soon", "have a good night", "thanks", "thank you", "awsome", "booster", "omicron",
                "flu", "flushot", "influenza", "monkeypox", "monkey pox", "children vaccine", "vaccine for children", 
                "vaccine for my 5-11 year old", "vaccine for my 6 months to 5-year-old", 
                "pay to receive the vaccine", "pay for vaccine", "pay for the vaccine", "vaccine cost",
                "pfizer", "moderna", "pregnant", "where is north york general hospital located", 
                "where is nygh located", "location of north york general hospital", 
                "location of nygh", "what is nygh location", "what is north york general hospital location",
                "helpline numbers", "on which  number i should call", "hospital number", "who can i call",
                "call", "nygh hospital number", "hospital contact", "how do i contact the hospital", 
                "how do i talk to a doctor","how do i talk to a professional", "contact hospital", "contact pharmacy"
                "what are the travel guidelines", "what are the different approved vaccines",
                "prophylaxis", "what if my pet becomes sick while i am isolating", "vaccination", "walk-in clinics",
                "walk in clinics", "vaccine", "pet becomes sick while i am isolating", "north york cough, cold and covid test clinic",
                "can i bring a support person or family member to my appointment", "what's your name?", "what is your name?", "what is your name", "what's your name"]
    
    helper = set()
    lowered_case = msg.lower()
    for KeyWord in KeyWords:
      helper.add(lowered_case.find(KeyWord))
    
    # for non-related questions
    if len(helper) == 1:
      return "Sorry, I don't understand your question. I can only answer questions related to Monkeypox, Influenza (Flu), and Covid-19. If you have any other questions, please contact NYGH's Pharmacy at (416)756-6666 or email them through NYGHPharmacy@nygh.on.ca", add_message
 
    ints = predict_class(msg, model)
    res, tag = getResponse(ints, intents)

    # Check if "Did I answer your question correctly?" needs to be added
    tags_to_avoid_adding = ["greeting", "chatbotname", "howareyou", "goodbye", "thanks", "noanswer", "options"]    
    if tag not in tags_to_avoid_adding:
        add_message = True

    return res, add_message

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
