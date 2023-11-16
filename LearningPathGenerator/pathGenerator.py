import requests
import json
import os
import re
from LearningPathGenerator.getAnswer import get_answer
from LearningPathGenerator.getPrompt import get_prompt_scale
from LearningPathGenerator.getPrompt import get_prompt_path
from LearningPathGenerator.Estimate import estimate, get_text
from LearningPathGenerator.createGraphy import create_graphy

class PathGenerator:
    question = ""

    def __init__(self, question, num = 1):
        self.question = question
        self.num = num

    def first_turn(self, num):
        self.prompt_scale = get_prompt_scale(self.question, num)
        self.result_scale = get_answer(self.prompt_scale)

    def select_best(self):
        matches = re.findall(r'\{.*?\}', self.result_scale)
        self.result_scale = estimate(get_text(self.question), matches)

    def transition(self):
        head = self.result_scale.find('{')
        end = self.result_scale.rfind('}')
        self.pool = eval(self.result_scale[head:end+1])
        keys = list(self.pool.keys())
        self.pool_str=str(keys)
    
    def second_turn(self):
        self.prompt_path = get_prompt_path(self.pool_str)
        self.result_path = get_answer(self.prompt_path)
        head = self.result_scale.find('[')
        end = self.result_scale.rfind(']')
        self.result_path = self.result_path[head:end+1]
