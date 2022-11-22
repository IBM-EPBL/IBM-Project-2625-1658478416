from django.shortcuts import render
from .forms import InputForm,DataForm
from .auth import *
import smtplib


def homepage(request):
    context ={}
    context['form']= DataForm()
    return render(request,'home.html',context)

def submit(request):
    context ={}
    context['form']= InputForm()
    email = request.POST.get('mail')
    password = request.POST.get('password')
    if(login(email,password)):
        print('OK')
        return homepage(request)

    else:
        print("Problem")
    return render(request, "index.html", context)

def signup_auth(request):
    context ={}
    context['form']= InputForm()
    email = request.POST.get('mail')
    password = request.POST.get('password')
    if(signup(email,password)):
        print('OK')
        sendmail(email)
        return homepage(request)

    else:
        print("Problem")
    return render(request, "signup.html", context)
def sendmail(receiver):
    
    gmail_user = 'mailpraveen927@gmail.com'
    gmail_password = 'voxbgsqlzujtjbfm'

    sent_from = gmail_user
    to = [receiver]
    subject = 'Smart Lender Verification Email'
    body = 'Thanks for using our service'

    email_text = """From: SmartLender
    
    This is an e-mail message
    """

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
def submitsign(request):
    context ={}
    context['form']= InputForm()
    email = request.POST.get('mail')
    password = request.POST.get('password')
    
    return render(request, "signup.html", context)

def index(request):
    context ={}
    context['form']= InputForm()
    return render(request, "index.html", context)
