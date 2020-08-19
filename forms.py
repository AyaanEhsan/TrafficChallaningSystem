from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=100)
    mobile = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=100)
    aadharno = forms.IntegerField()
    vehicleno = forms.CharField(max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class ComplaintForm(forms.Form):

    photo =forms.ImageField()
    description = forms.CharField(max_length=100)