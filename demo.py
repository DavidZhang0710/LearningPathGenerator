from LearningPathGenerator.pathGenerator import PathGenerator
from LearningPathGenerator.createGraphy import create_graphy
from LearningPathGenerator.Estimate import estimate, get_text

if __name__ == '__main__':
    question = "Learning English"
    pathGenerator = PathGenerator(question)
    pathGenerator.first_turn(3)
    pathGenerator.select_best()
    pathGenerator.transition()
    pathGenerator.second_turn()
    print(pathGenerator.result_path)