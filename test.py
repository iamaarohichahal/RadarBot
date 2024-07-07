from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
import nltk
import random

# Initialize NLTK tokenizer and download necessary data
nltk.download('punkt')

# Define responses for the bot
responses = {
    "greetings": ["Hello!", "Hi there!", "Hey!", "Hi! How can I help you?"],
    "name": ["My name is ChatBot.", "You can call me ChatBot.", "I'm ChatBot."],
    "age": ["I am ageless!", "I don't have an age.", "Age is just a number for me."],
    "fmcw": {
        "full form": "FMCW stands for Frequency-Modulated Continuous Wave.",
        "difference with CW": "Unlike CW radar, FMCW radar can change its operating frequency during measurement. This modulation in frequency or phase allows it to perform range measurements, which CW radar cannot do due to its inability to provide accurate timing for the transmit and receive cycle.",
        "technical feature": "FMCW radar can measure the range of targets by modulating the transmission signal in frequency or phase, creating a time reference for distance measurement through the frequency modulation of the transmitted signal.",
        "why CW cannot determine range": "Simple continuous wave radar devices cannot determine target range because they lack the timing mark necessary to accurately time the transmit and receive cycle, which is needed to convert this timing into range.",
        "frequency modulation for stationary objects": "In FMCW radar, a signal is transmitted that periodically increases or decreases in frequency. When an echo signal is received, the change in frequency experiences a delay (Δt) due to the runtime shift, similar to pulse radar. The distance measurement is then based on the differences in phase or frequency between the transmitted and received signals.",
        
    },
    "default": ["I'm sorry, I don't understand.", "Could you please rephrase?", "I'm not sure I follow."]
}

# Initialize Flask application
app = Flask(__name__)

# Define a function to process user input and return a response
import random

# Assuming responses dictionary is defined earlier as shown in previous responses

def get_bot_response(user_text):
    tokens = word_tokenize(user_text.lower())
    
    if any(word in tokens for word in ["hi", "hello", "hey", "greetings"]):
        return random.choice(responses["greetings"])
    elif any(word in tokens for word in ["name", "called", "designation"]):
        return random.choice(responses["name"])
    elif any(word in tokens for word in ["age", "old", "year"]):
        return random.choice(responses["age"])
    elif any(word in tokens for word in ["fmcw", "radar"]):
        # Check for specific queries related to FMCW radar
        for key, value in responses["fmcw"].items():
            if any(word in tokens for word in key.split()):
                return value
        return random.choice(list(responses["fmcw"].values()))  # Convert dict_values to list for random choice
    else:
        return random.choice(responses["default"])
# Define routes for the Flask application
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response_route():
    user_text = request.args.get('userMessage')
    bot_response = get_bot_response(user_text)
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)
