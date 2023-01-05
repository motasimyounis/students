from dataclasses import field
from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['Title','Description']
    
class DateInput(forms.DateTimeInput):
    input_type = 'date'
    

class HomeForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        widgets = {'Due':DateInput()}
        fields = ['Subject',
                  'Title',
                  'Description',
                  'Due',
                  'Status',
                  ]
        
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter your search : ")    



class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['Title','Status']
        
        
class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect) 

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    ) 
    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    ) 


class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    ) 
    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    ) 


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
            
 
        