from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class ReportsForm(forms.ModelForm):  
    class Meta:  
        model = Reports  
        fields = "__all__"  