import requests
import json
import os

from LearningPathGenerator.getAnswer import get_answer
from LearningPathGenerator.createGraphy import create_graphy

config_path = 'LearningPathGenerator/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)
[scale_schema_path, scale_ICL_path, schema_path, ICL_path] = [config["scale_schema_path"], config["scale_ICL_path"], config["schema_path"], config["ICL_path"]]

# question_0    第一次提问文本
# message_0
# result_0      第一次回答
# pool_0        回答的二维数组
# question_1    一维数组的文本
# message_1     
# result_1      第二次回答

class PathGenerator:
    question_0 = ""
    # message_0
    result_0 = ""
    result_0_list =[]
    pool_0_list =[]
    pool_0 = []
    question_1 = ""
    # message_1  
    result_1 = ""

    def __init__(self, question):
        self.question_0 = question

    def build_message(self, question, turn):
        if turn == 0:
            with open(scale_ICL_path, 'r', encoding='utf-8') as f:
                self.message_0 = json.load(f)
            self.message_0["messages"].append({
                "role": "user",
                "content": "以之前同样的格式回答：" + question
            })
            with open(scale_schema_path, 'r',encoding='utf-8') as f:
                scale_schema_prompt = f.read()
            self.message_0["messages"][0]["content"] = scale_schema_prompt + '\n' + self.message_0["messages"][0]["content"]
            self.message_0 = json.dumps(self.message_0)
        else:
            with open(ICL_path, 'r', encoding='utf-8') as f:
                self.message_1 = json.load(f)
            self.message_1["messages"].append({
                "role": "user",
                "content": "以之前同样的格式回答：" + question
            })
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_prompt = f.read()
            self.message_1["messages"][0]["content"] = schema_prompt + '\n' + self.message_1["messages"][0]["content"]
            self.message_1 = json.dumps(self.message_1)

    def build_pool_list(self):
        pool_list = []
        for result in self.result_0_list:
            pool=[]
            list=result.split('\n')
            for word in list:
                units=word.split('\'')
                i=0
                out_unit=[]
                include=[]
                for unit in units:
                    if i%2==1:
                        if i==1:
                            out_unit.append(unit)
                        else:
                            include.append(unit)
                    i=i+1
                out_unit.append(include)
                pool.append(out_unit)
            pool_list.append(pool)
        self.pool_0_list = pool_list


    def prebuild_for_next_turn(self):
        out=[]
        knowledge_set=""
        list=self.result_0.split('\n')
        for word in list:
            units=word.split('\'')
            i=0
            out_unit=[]
            include=[]
            for unit in units:
                if i%2==1:
                    if i==1:
                        out_unit.append(unit)
                    else:
                        include.append(unit)
                i=i+1
            out_unit.append(include)
            out.append(out_unit)
        for i in range(len(out)):
            if i==0:
                knowledge_set=knowledge_set+out[i][0]
            else:
                knowledge_set=knowledge_set+','+out[i][0]
        self.pool_0 = out
        self.question_1 = knowledge_set


if __name__ == '__main__':
    question = "如何学习数据结构"
    obj = PathGenerator(question)

    obj.build_message(obj.question_0, 0)
    obj.result_0 = get_answer(obj.message_0)
    obj.prebuild_for_next_turn()

    obj.build_message(obj.question_1, 1)
    obj.result_1 = get_answer(obj.message_1)

    create_graphy(obj.pool_0, obj.result_1)
