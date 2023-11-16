import requests
import json
import os

config_path = 'LearningPathGenerator/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)
[API_KEY, SECRET_KEY] = [config["API_KEY"], config["SECRET_KEY"]]
os.environ['API_KEY'] = API_KEY
os.environ['SECRET_KEY'] = SECRET_KEY

def get_access_token():
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+API_KEY+"&client_secret="+SECRET_KEY
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_prompt_scale(question, num):
        
    url = "https://aip.baidubce.com/rest/2.0/wenxinworkshop/api/v1/template/info?access_token=" + get_access_token() + "&id=11278&question=" + question + "&num=" + str(num)

    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    json_res = json.loads(response.text)
    if 'error' in json_res:
        return 'ERROR: ' + json_res['error_code']
    print(json_res)
    return json_res['result']['content']

def get_prompt_path(pool):
        
    url = "https://aip.baidubce.com/rest/2.0/wenxinworkshop/api/v1/template/info?access_token=" + get_access_token() + "&id=11279&pool=" + pool

    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    json_res = json.loads(response.text)
    if 'error' in json_res:
        return 'ERROR: ' + json_res['error_code']
    print(json_res)
    return json_res['result']['content']