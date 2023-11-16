import json
import os
import datetime
from LearningPathGenerator.pathGenerator import PathGenerator
from LearningPathGenerator.createGraphy import create_graphy
from LearningPathGenerator.Estimate import estimate, get_text

if __name__ == '__main__':
    question = "学习英语"
    obj = PathGenerator(question)
    obj.first_turn(3)
    obj.select_best()
    obj.transition()
    obj.second_turn()
    print(obj.result_path)