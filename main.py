import json
import os
import datetime
from LearningPathGenerator.pathGenerator import PathGenerator
from LearningPathGenerator.createGraphy import create_graphy
from LearningPathGenerator.getAnswer import get_answer
from LearningPathGenerator.Estimate import estimate, get_text
from flask import Flask, request, render_template, Response

app = Flask(__name__, template_folder='templates')

CALL_TIME = 3

debug_flag = False

@app.route('/')
def generate_html():
    input_str = request.args.get('input')  # 获取用户输入的参数
    flag = request.args.get('checked')
    if flag == 'false':
        obj = PathGenerator(input_str)

        obj.build_message(obj.question_0, 0)
        obj.result_0 = get_answer(obj.message_0)
        obj.prebuild_for_next_turn()

        obj.build_message(obj.question_1, 1)
        obj.result_1 = get_answer(obj.message_1)

        create_graphy(obj.question_0, obj.pool_0, obj.result_1)
        # return render_template('render.html')

    else:
        return "现使用API不支持多token生成，因此暂不开放BERT"
        obj = PathGenerator(input_str)

        obj.build_message(obj.question_0, 0)

        ref_text = get_text(obj.question_0)

        for i in range(CALL_TIME):
            obj.result_0_list.append(get_answer(obj.message_0))
        obj.build_pool_list()
        pos = estimate(ref_text, obj.pool_0_list)
        obj.result_0 = obj.result_0_list[pos]

        obj.prebuild_for_next_turn()

        obj.build_message(obj.question_1, 1)
        obj.result_1 = get_answer(obj.message_1)

        create_graphy(obj.question_0, obj.pool_0, obj.result_1)

    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S_image.jpg")

    with open('temp.jpeg', 'rb') as f:
        image = f.read()
    with open('C:/Users/Administrator/Desktop/project/temp_image/' + filename, 'wb') as output_file:
        output_file.write(image)
    return Response(image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = debug_flag)