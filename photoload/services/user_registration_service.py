from django import forms
from django.contrib.auth.hashers import make_password
from service_objects.services import Service

from photoload.models import User


class RegisterUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    photo = forms.ImageField()
    age = forms.CharField()

    def process(self):
        self.result = self._user
        return self

    @property
    def _user(self):
        return User.objects.create(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=make_password(self.cleaned_data.get('password')),
            photo=self.cleaned_data.get('photo'),
            age=self.cleaned_data.get('age')
        )
