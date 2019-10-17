from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    user_name = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='E-Mail', max_length=100)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)