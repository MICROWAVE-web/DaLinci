from django import forms
from django.contrib.auth import get_user_model

from Main.models import AbbreviatedLink, User

CHOICES = [('email', ' By Email'),
           ('sms', ' By SMS')]


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat', widget=forms.PasswordInput)
    # type_of_confirmation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,
    #                                          label='Тип подтверждения регистрации:')

    class Meta:
        model = get_user_model()
        fields = ('email',)
        # fields = ('email', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ServiceForm(forms.ModelForm):
    parent_link = forms.CharField(max_length=300, widget=forms.URLInput(
        attrs={'class': 'bg-purple-white shadow rounded border-0 p-3 form_input mobile_form_input',
               'placeholder': 'Введите ссылку'}), label='')

    class Meta:
        model = AbbreviatedLink
        fields = ('parent_link',)


class SMSForm(forms.ModelForm):
    personal_sms_code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter code'}),
                                           label='SMS-code')

    class Meta:
        model = User
        fields = ('personal_sms_code',)
