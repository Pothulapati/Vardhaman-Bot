import json

from rasa_nlu.model import Interpreter

class Data:
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return str(self.data)
    
    def get_intent(self):
        return self.data['intent']['name']
    
    def get_confidence(self):
        return self.data['intent']['confidence']

    def get_entities(self):
        return dict(map((lambda x : (x['entity'], x['value'])), self.data['entities']))
    
    def has_intent(self, *intents):
        if self.get_intent() in intents:
            return True
        else:
            return False
            
class Engine:
    def __init__(self, models_path = "./models/current/nlu"):
        self.interpreter = Interpreter.load(models_path)
    
    def parse(self, message):
        return Data(self.interpreter.parse(message))