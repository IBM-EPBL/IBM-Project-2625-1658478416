import flask
import joblib
import numpy as np
from flask import render_template, request
from flask_cors import CORS

import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "zJXNS7RuxksoVPyMjZDER8bqMSbF3OvzzuZZWw5FnpMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__,template_folder='template')
CORS(app)
 
@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('home.html')
@app.route('/index', methods=['GET'])
def sendRegistrationPage():
    return render_template('index.html')
@app.route('/output', methods = ['POST'])
def prediction():
	if request.method == 'POST':
		gender = request.form['gender']
		married = request.form['status']
		dependat =request.form['dependants']
		education = request.form['education']
		employ = request.form['employ']
		annual_income = request.form['aincome']
		co_income = request.form['coincome']
		Loan_amount = request.form['Lamount']
		Loan_amount_term = request.form['Lamount_term']
		credit = request.form['credit']
		proper = request.form['property_area']

	gender = gender.lower()
	married= married.lower()
	education = education.lower()
	employ = employ.lower()
	proper = proper.lower()
	if(employ=='yes'):
		employ = 1
	else:
		employ = 0
	if(gender=='male'):
		gender = 1
	else:
		gender = 0
	if (married=='married'):
		married=1
	else:
		married=0
	if (proper=='rural'):
		proper=0
	elif (proper=='semiurban'):
		proper=1
	else:
		proper=2
	if (education=='graduate'):
		education=0
	else:
		education=1
    
	dependat = int(dependat)
	annual_income = int(annual_income)
	co_income = int(co_income)
	Loan_amount = int(Loan_amount)
	Loan_amount_term = int(Loan_amount_term)
	credit = int(credit)
	#x =np.array([[0,gender, married, dependat,education,employ,annual_income,co_income,Loan_amount,Loan_amount_term,credit,proper]])
	x =[0,gender, married, dependat,education,employ,annual_income,co_income,Loan_amount,Loan_amount_term,credit,proper]
	#model = joblib.load('R.pkl')
	
	#ans = int(model.predict(x)[0])
	#if (ans==1):
		#print("You are eligible. Kindly wait for further notice")
	#else:
		#print("Your application status did not match our criteria")

	payload_scoring = {"input_data": [{"field": ["","Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"], "values": [[0,0,0,0,0,0,4547,0.0,115.0,360,1,1], [0,0,0,0,0,0,4947,0.0,105.0,361,1,1]]}]}

	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/77f857ff-c248-41f7-b24f-2a3128ac1906/predictions?version=2022-11-22', json=payload_scoring,
	headers={'Authorization': 'Bearer ' + mltoken})
	print("Scoring response")
	pred = response_scoring.json()
	p = pred['predictions'][0]['values'][0][0]
	if(pred == 0):
		print("You are not eligible")
	else:
		print("You are eligible")
	
	return render_template('output.html', output=p)

if __name__ == '__main__':
	app.debug = True
	app.run()
 