import flask
import joblib
import numpy as np
from flask import render_template, request
from flask_cors import CORS

import smtplib
import requests
import json

import pyrebase


firebaseConfig = {
  'apiKey' : "AIzaSyBwc1_f3i-y3W2ClhX6BimI3rJd9YrbDjw",
  'authDomain' : "smart-lender-1639b.firebaseapp.com",
  'projectId' : "smart-lender-1639b",
  'storageBucket' : "smart-lender-1639b.appspot.com",
  'messagingSenderId' : "89081040576",
  'appId' : "1:89081040576:web:9e721303632308e2646725",
  'measurementId' : "G-F3C4GXSCC0",
  'databaseURL' : "none"
}


firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def sendmail(receiver):
    gmail_user = 'mailpraveen927@gmail.com'
    gmail_password = 'xxxxxxxx'
    sent_from = gmail_user
    to = [receiver]
    from_ = "From: {}".format(sent_from)
    to_ = "To: {}".format(receiver)
    subject = "Subject: Smart Lender Verification Email"
    body = "Thanks for using our service"
    message = from_ + "\n" + to_ + "\n" + subject + "\n" + body


    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, message)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

def login(email,password):
	try:
		login = auth.sign_in_with_email_and_password(email,password)
		print("Successfully logged in!")
		return 1
	except Exception as e:
		t = json.loads(e.args[1])
		if(t['error']['errors'][0]['message']=="EMAIL_NOT_FOUND"):
			return signup(email,password)
		return 0
		
def signup(email,password):
    try:
        user = auth.create_user_with_email_and_password(email,password)
        sendmail(email)
        return 1

    except Exception as e:
        #t = json.loads(e.args[1])
        #print(t['error']['code'])
        print(e)
        return 0



def submit(email,password):
    if(login(email,password)):
        return 1
    else:
        print("Problem")
        return 0
    

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "zJXNS7RuxksoVPyMjZDER8bqMSbF3OvzzuZZWw5FnpMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__,template_folder='template')
CORS(app)
 

@app.route('/', methods=['GET'])
def sendLoginPage():
    return render_template('login.html')
@app.route('/home', methods=['POST'])
def sendHomePage():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if(submit(email,password)):
			return render_template('home.html')
	return render_template('login.html')

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
	# model = joblib.load('R.pkl')
	
	# ans = int(model.predict(x)[0])
	# if (ans==1):
	# 	print("You are eligible. Kindly wait for further notice")
	# else:
	# 	print("Your application status did not match our criteria")

	payload_scoring = {"input_data": [{"field": ["","Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"], "values": [x]}]}

	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/77f857ff-c248-41f7-b24f-2a3128ac1906/predictions?version=2022-11-22', json=payload_scoring,
	headers={'Authorization': 'Bearer ' + mltoken})
	print("Scoring response")
	pred = response_scoring.json()
	p = pred['predictions'][0]['values'][0][0]
	if(p == 0):
		print("Your application status did not match our criteria")
	else:
		print("You are eligible. Kindly wait for further notice")
	
	return render_template('output.html', output=p)

if __name__ == '__main__':
	app.debug = True
	app.run()
 