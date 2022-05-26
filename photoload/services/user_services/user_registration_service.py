from django import forms
from django.contrib.auth.hashers import make_password
from service_objects.services import Service

from photoload.models import User


class RegistrationUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    photo = forms.ImageField(required=False)
    age = forms.CharField(required=False)
    error_report = []

    def process(self):
        import pdb
        pdb.set_trace()
        if self._is_valid():
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

    def _is_valid(self):
        self._checking_the_uniqueness_username()
        self._checking_the_uniqueness_email()
        return not bool(self.error_report)

    def _checking_the_uniqueness_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')):
            self.error_report.append('username_not_unique')

    def _checking_the_uniqueness_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')):
            self.error_report.append('email_not_unique')
