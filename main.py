import datetime
from LearningPathGenerator.pathGenerator import PathGenerator
from LearningPathGenerator.createGraphy import create_graphy
from flask import Flask, request, render_template, Response

app = Flask(__name__, template_folder='templates')

CALL_TIME = 3

debug_flag = False

@app.route('/')
def generate_html():
    input_str = request.args.get('input')
    flag = request.args.get('checked')
    pathGenerator = PathGenerator(input_str)
    if flag == 'false':
        pathGenerator.first_turn(1)
    else:
        pathGenerator.first_turn(5)
    pathGenerator.transition()
    pathGenerator.second_turn()
    print(pathGenerator.result_path)
    create_graphy(pathGenerator.question_0, pathGenerator.pool_0, pathGenerator.result_1)

    # History
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S_output.jpg")
    with open('output.jpeg', 'rb') as f:
        image = f.read()
    with open('path/for/history' + filename, 'wb') as output_file:
        output_file.write(image)
    return Response(image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = debug_flag)