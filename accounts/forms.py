from django.contrib.auth import authenticate
from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Employee


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        exclude = ['documents', 'resume','user','is_active','joining_date',]


class SignupForm(UserCreationForm):

    # name = forms.CharField(label='Name')
    username = forms.CharField(max_length=20)
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean_username(self):
        user_type = self.cleaned_data.get('user_type')

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        return user_type

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean(self):

        clean_data = self.cleaned_data
        self.errors.as_data()
        return clean_data

    def save(self, commit=False):
        username = self.cleaned_data.get('username')
        valid_username = self.clean_username()

        if username == valid_username:
            form = super(SignupForm, self).save(commit=commit)
            # data = self.cleaned_data
            form.username = username  # update user with unique username
            form.save()
            return form
        return valid_username


class LoginForm(forms.Form):

    username = forms.CharField(label='Email')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.user_cache = None
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        # phone_number = full_phone_number(cd.get('phone_number'))
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if User.objects.filter(username=username).exists():

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                self.add_error('password', "Please enter a correct password.")
        else:
            self.add_error('username', 'User name not exists. Please check user name.')
        return cd

    def get_user(self):
        return self.user_cache