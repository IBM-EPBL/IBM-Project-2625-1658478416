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


def login(email,password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        return 1
    except:
        print("Invalid email or password")
        return 0


def signup(email,password):
    try:
        user = auth.create_user_with_email_and_password(email,password)
        return 1

    except Exception as e:
        #t = json.loads(e.args[1])
        #print(t['error']['code'])
        print(e)
        return 0