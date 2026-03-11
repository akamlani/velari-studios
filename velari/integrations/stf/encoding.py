import numpy as np
from   sentence_transformers import SentenceTransformer

class Encoder(object):
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # 'bert-base-nli-mean-tokens'
        self.model = SentenceTransformer(model_name)

    def encode(self, sentences, **kwargs) -> np.ndarray:
        return self.model.encode(sentences, **kwargs)
