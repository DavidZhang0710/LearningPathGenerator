# LearningPathGenerator

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/DavidZhang0710/LearningPathGenerator/blob/main/LICENSE)

A python project to generate a learning path on a specific topic or question. Using the ***LLMs*** API and ***MPNet*** model to automatically create a learning path chart for a question in '***HOW TO ... ?***' form.

## Project Introduction
Nowadays, more and more LLMs are trained to deal various kinds of problems, like ***Recommendation System*** or ***text translation***, but we can see that most of these model work badly with the ***deep-logical-chain*** task.

***Program-aided Language*** (PAL) Models are invented to deal with this kind of deep-logical-chain problems, which involve program to do the calculate process to ensure the accuracy. This project also apply this model to deal with the logical problems.

***Learning path*** is a logical path along which you can learn to solve a problem on a roll. This project help you to build a learning path on most kinds of problems.

## Project Requirement
Python3

Flask==2.3.3

matplotlib==3.7.1

networkx==3.0

Requests==2.31.0

scikit_learn==1.2.1

sentence_transformers==2.2.2

## Quick Start

1. Clone this repo and required python modules

   ```bash
   git clone https://github.com/DavidZhang0710/LearningPathGenerator.git
   cd ./LearningPathGenerator
   pip install -r requirements.txt
   ```

2. Download MPNet model

   The default MPNet model is [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), which can be downloaded form huggingface and loaded by a python module named ***SentenceTransformer***.

   ```bash
   cd ./LearningPathGenerator
   git submodule update --init --recursive
   ```

   And if you want to use other SentenceTransformer, you can download it and replace the code fragment below in LearningPathGenerator/Estimate.py.

   ```python
   def estimate(reference_text,pool_list):
       model = SentenceTransformer('path/to/your/model')
   ```

   But make sure that can be identified by *SentenceTransformer()*.

3. Apply LLMs API (or local model)
   
   The LLMs API used in this project is ***ERNIE Bot*** developed by Baidu, you can surface their website to get an API_KEY along with an SECRET_KEY, which will be used later.
   
   After you finished the step 1, you can find *LearningPathGenerator/config.json*, you are supposed to replace the values of "API_KEY" and "SECRET_KEY" with those you have got.
   
   Example given below:
   
   ```json
   {
       "API_KEY" : "YOUR_API_KEY",
       "SECRET_KEY" : "YOUR_SECRET_KEY"
   }
   ```
   
   Similarly, if you want to use other LLMs API, you can adapt the ***get_answer()*** in *LearningPathGenerator/getAnswer.py* to your own version, but remember that you should keep the input and output form same with the original version.

4. Demo

   If you want to experience a small demo of this project, you can click ***[here](http://124.221.34.139/projects/pathgenerator.html)*** to turn to a web demo.

## More Details

#### Generating steps

The total steps of generating a learning path is about to be three.

- Fetch relevant knowledge scales to the given topic by ***LLMs***, including their child knowledge points.
- Fetch the relationships between these knowledge points by ***LLMs***, and select the most logical answer by ***MPNet***.
- Create a chart by ***networkx*** using the knowledge pool and relationships.
