from django.db.models.base import Model
from django.forms import ModelForm
from django.core.exceptions import ValidationError
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

    def clean(self):
        super(SessionCreateForm, self).clean()
        hall_name = self.cleaned_data['hall_name']
        start_session_time = self.cleaned_data['start_session_time']
        end_session_time = self.cleaned_data['end_session_time']
        date_start_show = self.cleaned_data['date_start_show']
        date_end_show = self.cleaned_data['date_end_show']
        on_air = Sessions.objects.filter(hall_name=hall_name)
        for i in on_air:
            if  i.start_session_time <= start_session_time <= i.end_session_time and \
                i.date_start_show <= date_start_show <= i.date_end_show or \
                i.start_session_time <= end_session_time <= i.end_session_time and \
                i.date_start_show <= date_end_show <= i.date_end_show:
                raise ValidationError('This hall doesnt exists')

        if start_session_time > end_session_time or date_start_show > date_end_show:
            raise ValidationError('Session start cannot be greater than the end')


class HallsCreateForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'size']

       
class MoviesCreateForm(ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'description']


class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(label='Sorted ', choices=[('Time', 'By start time'), \
        ('PriceLH', 'Price: low to high'),('PriceHL', 'Price: high to Low')])

class PurchaseForm(ModelForm):
    quantity = forms.IntegerField(min_value=1)
    class Meta:
        model = Purchase
        fields = ['quantity',]