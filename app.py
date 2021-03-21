########  imports  ##########
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)
import json
#############################
# Additional code goes here #

def getJsonFile():
    with open('details.json') as json_file: 
        data = json.load(json_file) 
        json_details = data['details'] 
        return json_details

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        message = getJsonFile()
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200

#############################
#########  run app  #########
app.run(debug=True)