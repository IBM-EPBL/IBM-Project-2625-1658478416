from django.shortcuts import render
from .forms import InputForm
from .auth import *

def submit(request):
    context ={}
    context['form']= InputForm()
    email = request.POST.get('mail')
    password = request.POST.get('password')
    if(signup(email,password)):
        print("OK")
    else:
        print("Problem")
    return render(request, "index.html", context)

def index(request):
    context ={}
    context['form']= InputForm()
    return render(request, "index.html", context)
