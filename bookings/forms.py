from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)

    def clean_number_of_seats(self):
        seats = self.cleaned_data.get('number_of_seats')
        if seats < 1:
            raise forms.ValidationError("Minimum 1 seat must be booked.")
        if self.travel_option and seats > self.travel_option.available_seats:
            raise forms.ValidationError("Not enough seats available.")
        return seats

