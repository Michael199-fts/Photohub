from django import forms
from django.contrib.auth.hashers import make_password
from service_objects.services import Service

from photoload.models import User


class RegistrationUserService(Service):
    username = forms.CharField(initial=None, required=False)
    first_name = forms.CharField(initial=None, required=False)
    last_name = forms.CharField(initial=None, required=False)
    email = forms.EmailField(initial=None,required=False)
    password = forms.CharField(initial=None, required=False)
    photo = forms.ImageField(initial=None, required=False)
    age = forms.IntegerField(initial=None, required=False)
    validations = ['_checking_the_uniqueness_username', '_checking_the_uniqueness_email', '_checking_missed_fields']

    def process(self):
        import pdb
        pdb.set_trace()
        if not self._error_report:
            self.result = self._user
            self.error_report = []
        else:
            self.error_report = self._error_report
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

    @property
    def _error_report(self):
        error_report = []
        for validation in self.validations:
            if getattr(self, validation)():
                error_report.append(getattr(self, validation)())
        return error_report

    def _checking_the_uniqueness_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')):
            return 'username_not_unique'

    def _checking_the_uniqueness_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')):
            return 'email_not_unique'

    def _checking_missed_fields(self):
        errors = []
        for el, val in self.cleaned_data.items():
            if val == '':
                errors.append(el)
        if errors == []:
            return None
        else:
            return "Fields missed: " + str(errors)