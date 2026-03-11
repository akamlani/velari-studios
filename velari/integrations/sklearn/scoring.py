import numpy as np
import sklearn.metrics as met

def scorer_cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    # a.reshape(1, -1) to make it 2D for sklearn
    # b.reshape(1, -1) to make it 2D for sklearn
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)
    return round( float(met.pairwise.cosine_similarity(a, b)[0][0]), 4)