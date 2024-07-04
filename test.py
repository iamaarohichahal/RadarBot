

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import spacy

# Load the spaCy model explicitly using its package name
nlp = spacy.load('en')

# Create a new ChatBot instance with BestMatch logic adapter
bot = ChatBot(
    "RadarBot",
    read_only=False,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.SpacySimilarity',
            'tagger_language': nlp
        }
    ]
)

# Training data for the chatbot
list_to_train = [
    "hi",
    "Hello there! How can I be of assistance?",
    "what's your name?",
    "My name is RadarBot",
    "how old are you",
    "I am ageless"
]

# Create a ListTrainer instance and train the chatbot
list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)
