########### Python Form Recognizer Async Analyze #############
import json
import time
from requests import get, post
########  imports  ##########
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

# Endpoint URL
endpoint = r"https://newformrecog.cognitiveservices.azure.com"
apim_key = "8de9ea6fece649a29bc70b3d17330630"
model_id = "1b7332d3-14f7-49fd-8acd-cc97e4b69928"
post_url = endpoint + "/formrecognizer/v2.0/custom/models/%s/analyze" % model_id
source = r"C:\Users\Arun Korade\Downloads\test data\Sample_7.pdf"
params = {
    "includeTextDetails": True
}

headers = {
    # Request headers
    'Content-Type': 'application/pdf',
    'Ocp-Apim-Subscription-Key': apim_key,
}
with open(source, "rb") as f:
    data_bytes = f.read()

try:
    resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % json.dumps(resp.json()))
        quit()
    print("POST analyze succeeded:\n%s" % resp.headers)
    get_url = resp.headers["operation-location"]
except Exception as e:
    print("POST analyze failed:\n%s" % str(e))
    quit() 

def createExcel(resp_json):
    # area = resp_json['pageResults']['tables']['cells']
   # rows =  resp_json['pageResults']['tables']['rows']
   # cols =  resp_json['pageResults']['tables']['cols']
    # for i in rows*cols
        
    date = resp_json['createdDateTime']
    str_json = json.dumps(resp_json)
    value = str_json.find('Creatinine')
    new_json = str_json[value:]
    new_value = new_json.find('text')
    final_json = new_json[new_value+6:]
    final_value = final_json.find('text')
    le_value = final_json[final_value+8:final_value+11]
    print("\n\n\nfinal value: %s" % le_value)
    print("\n\n\date: %s" % date)

    result_json = {"label": date, "y": float(le_value)}
    str_json = json.dumps(result_json, indent = 4)

    with open('details.json') as json_file: 
        data = json.load(json_file) 
        temp = data['details'] 
        temp.append(result_json) 
    write_json(data)   

    # function to add to JSON 
def write_json(data, filename='details.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
      

n_tries = 15
n_try = 0
wait_sec = 5
max_wait_sec = 60
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = resp.json()
        if resp.status_code != 200:
            print("GET analyze results failed:\n%s" % json.dumps(resp_json))
            quit()
        status = resp_json["status"]
        if status == "succeeded":
            print("Analysis succeeded:\n%s" % json.dumps(resp_json))
            # Writing to sample.json 
            createExcel(resp_json)
            print("\n\n\nresp: \n%s " % resp_json['analyzeResult']['version'])
            quit()
        if status == "failed":
            print("Analysis failed:\n%s" % json.dumps(resp_json))
            quit()
        # Analysis still running. Wait and retry.
        time.sleep(wait_sec)
        n_try += 1
        wait_sec = min(2*wait_sec, max_wait_sec)     
    except Exception as e:
        msg = "GET analyze results failed:\n%s" % str(e)
        print(msg)
        quit()
print("Analyze operation did not complete within the allocated time.")


