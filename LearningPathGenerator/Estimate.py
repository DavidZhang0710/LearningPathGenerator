import os
from LearningPathGenerator.getAnswer import get_answer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np

def get_text(topic):
    result = get_answer(topic + "的学习步骤")
    return result

def estimate(text, pool_list):
    model = SentenceTransformer('LearningPathGenerator/model/all-mpnet-base-v2')
    max_score = 0
    best = dict()
    for pool in pool_list:
        data = eval(pool)
        all_strings = list(data.keys()) + [item for sublist in data.values() for item in sublist] + [text]
        embeddings = model.encode(all_strings)
        similarities = np.dot(embeddings[:-1], embeddings[-1].T)
        similarity_score = np.mean(similarities)
        print(similarity_score)
        if similarity_score > max_score:
            max_score = similarity_score
            best = data
    return best