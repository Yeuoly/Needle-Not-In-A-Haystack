from dotenv import load_dotenv
from tqdm import tqdm

from needle_not_in_a_haystack import NeedleNotInAHaystack
from utils import load_models

if __name__ == "__main__":
    load_dotenv()
    models = load_models("models", NeedleNotInAHaystack)

    for model in tqdm(models):
        model_instance = model()
        model_instance.test()
