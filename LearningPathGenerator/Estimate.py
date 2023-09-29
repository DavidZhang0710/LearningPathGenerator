import os
from LearningPathGenerator.getAnswer import get_answer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

def get_text(topic):
    message = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": topic + "的步骤"
            }
        ]
    })
    result = get_answer(message)
    return result

def estimate(reference_text,pool_list):
    model = SentenceTransformer('LearningPathGenerator/model/all-mpnet-base-v2')
    max_score = 0
    pos = 0
    for j in range(len(pool_list)):
        parent_pool=[]
        keyword_groups = []

        for i in pool_list[j]:
            parent_pool.append(i[0])

        keyword_groups.append(parent_pool)

        

        texts = [reference_text] + [" ".join(keywords) for keywords in keyword_groups]

        sentence_embeddings = model.encode(texts)

        similarity_score=0
        for i, keywords in enumerate(keyword_groups, start=1):
            keyword_embeddings = sentence_embeddings[i]
            reference_embeddings = sentence_embeddings[0]
            similarity_score = cosine_similarity([reference_embeddings], [keyword_embeddings])[0][0]
        if similarity_score > max_score:
            max_score = similarity_score
            pos = j
    return pos


if __name__ == "__main__":
    topic='制作智能小车'
    pool=[['机器视觉', ['图像处理','图像识别']], ['机器学习', []], ['深度学习', []], ['运动控制', ['避障','路径规划']], ['硬件', ['电机控制','传感器接口']]]
    score = estimate(get_text(topic),pool)
    print(score)