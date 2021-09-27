from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from cinema.models import MyUser, Hall, Movies, Sessions, Purchase


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'spent']

class SessionCreateForm(ModelForm):

    class Meta:
        model = Sessions
        fields = ('movie_title', 'hall_name', 'start_session_time', 'end_session_time', 
                  'date_start_show', 'date_end_show', 'price' )
        widgets = {
            'start_session_time': forms.TimeInput(attrs={'type': 'start_session_time'}),
            'end_session_time': forms.TimeInput(attrs={'type': 'end_session_time'}),
            'date_start_show': forms.DateInput(attrs={'type': 'date_start_show'}),
            'date_end_show': forms.DateInput(attrs={'type': 'date_end_show'}),
        }
       

class HallsCreateForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'size']
       
class MoviesCreateForm(ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'duration', 'description']

class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(label='Sorted ', choices=[('Time', 'By start time'), \
        ('PriceLH', 'Low to high'),('PriceHL', 'High to Low')])

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity']