from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Owner
from cats.models import Cat


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    age = forms.IntegerField(required=False)

    class Meta:
        model = Owner
        fields = ('username', 'email', 'age', 'password1', 'password2')


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ('name', 'breed', 'age')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ('email', 'age', 'first_name', 'last_name')
