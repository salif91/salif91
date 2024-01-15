from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)    
    username = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class AddSchoolForm(forms.Form):
    enom = forms.CharField(max_length=50)
    ville = forms.CharField(max_length=50)
class AddStudentForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    adresse = forms.CharField(max_length=50)
    telephone = forms.CharField(max_length=12)
    