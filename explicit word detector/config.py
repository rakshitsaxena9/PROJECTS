import os

class Config:
    DEBUG = True
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
