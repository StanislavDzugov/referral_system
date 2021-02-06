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

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError as e:
            try:
                del e.error_dict['phone_number']
            except:
                pass
            self._update_errors(e)
