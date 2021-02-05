from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from user_profile.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField


class CreateUserForm(ModelForm):
    """
        :param username: we use it for phone_number
    """

    phone_number = PhoneNumberField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Phone number (Example: +79646212313)',
        'class': 'form-control',
    }))

    class Meta:
        model = CustomUser
        fields = ['phone_number']
