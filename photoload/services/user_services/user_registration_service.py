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
        if self.error_report == []:
            self.result = self._user
        return self


    @property
    def _user(self):
        if self.checking_the_uniqueness:
            try:
                return User.objects.create(
                    username=self.cleaned_data.get('username'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email=self.cleaned_data.get('email'),
                    password=make_password(self.cleaned_data.get('password')),
                    photo=self.cleaned_data.get('photo'),
                    age=self.cleaned_data.get('age')
                )
            except:
                self.error_report.append('user_create_err')


    @property
    def checking_the_uniqueness(self):
        check_answer = True
        try:
            if bool(User.objects.all().filter(username=self.cleaned_data.get('username'))):
                self.error_report.append('username_not_unique')
                check_answer = False
            if bool(User.objects.all().filter(email=self.cleaned_data.get('email'))):
                self.error_report.append('email_not_unique')
                check_answer = False
        except:
            pass
        return check_answer
