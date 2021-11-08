from django import forms
from django.contrib.auth import get_user_model

from Main.models import AbbreviatedLink


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ServiceForm(forms.ModelForm):
    parent_link = forms.CharField(max_length=300, widget=forms.URLInput(attrs={'class': 'bg-purple-white shadow rounded border-0 p-3 form_input', 'placeholder': 'Введите ссылку'}), label='')

    class Meta:
        model = AbbreviatedLink
        fields = ('parent_link',)
