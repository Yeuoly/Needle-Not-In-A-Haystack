import importlib
import inspect
import os
import random
from typing import TypeVar


nouns = ["cat", "dog", "man", "woman", "boy", "girl", "bird", "car", "tree", "house", "mouse", "book", "computer", "apple", "banana", "student", "teacher", "doctor", "nurse"]
verbs = ["runs", "jumps", "flies", "drives", "eats", "sleeps", "talks", "reads", "writes", "plays", "sings", "dances", "thinks", "learns", "teaches", "builds", "cooks", "paints", "draws"]
adjectives = ["quick", "lazy", "happy", "sad", "fast", "slow", "loud", "quiet", "beautiful", "ugly", "smart", "dumb", "bright", "dark", "tall", "short", "big", "small", "young", "old"]
adverbs = ["quickly", "slowly", "happily", "sadly", "loudly", "quietly", "gracefully", "angrily", "eagerly", "carefully", "carelessly", "bravely", "fearfully", "generously", "selfishly", "politely", "rudely", "honestly", "dishonestly"]

def generate_sentence():
    subject = random.choice(nouns)
    verb = random.choice(verbs)
    adj = random.choice(adjectives)
    adv = random.choice(adverbs)
    
    sentence = f"The {adj} {subject} {adv} {verb}."
    return sentence

T = TypeVar("T")

def load_models(model_path: str, parent_type: T) -> list[T]:
    """
    Load models from a given path.
    """
    models = []
    for file in os.listdir(model_path):
        if file.endswith(".py"):
            module_name = file[:-3]
            module = importlib.import_module(f"{model_path}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, parent_type) and obj != parent_type:
                    models.append(obj)
    return models