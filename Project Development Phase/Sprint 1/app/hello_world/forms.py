from django import forms
  
# creating a form 
class InputForm(forms.Form):
  
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"User name / Email"}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Password"}))
    