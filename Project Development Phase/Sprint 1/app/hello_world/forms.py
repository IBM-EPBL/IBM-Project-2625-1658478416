from django import forms
  
# creating a form 
class InputForm(forms.Form):
  
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"User name / Email"}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Password"}))

class DataForm(forms.Form):
  
    Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"User name / Email"}))
    Age = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Age"}))
    Gender = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Gender"}))
    Married = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Married"}))
    Dependents = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Dependents"}))
    Education = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Education"}))
    Self_Employed = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Self_Employed"}))
    ApplicantIncome = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"ApplicantIncome"}))
    CoapplicantIncome = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"CoapplicantIncome"}))
    LoanAmount = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"LoanAmount"}))
    Property_Area = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Property_Area"}))
    Loan_Status = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input','placeholder':"Loan_Status"}))
    