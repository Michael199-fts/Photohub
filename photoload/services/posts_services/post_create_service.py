from django import forms
from service_objects.services import Service
from photoload.models import Post, User


class CreatePostService(Service):
    title = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    text = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    validations = ['_checking_missed_fields']

    def process(self):
        if not self._error_report:
            self.result = self._post
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self
    
    @property
    def _post(self):
        return Post.objects.create(
            title=self.cleaned_data.get('title'),
            author=User.objects.get(id=self.cleaned_data.get('user_id')),
            text=self.cleaned_data.get('text'),
            rating=0,
            photo=self.cleaned_data.get('photo')
        )

    @property
    def _error_report(self):
        error_report = []
        for validation in self.validations:
            if getattr(self, validation)():
                error_report.append(getattr(self, validation)())
        return error_report

    def _checking_missed_fields(self):
        errors = []
        for el, val in self.cleaned_data.items():
            if val == '':
                errors.append(el)
        if errors == []:
            return None
        else:
            return "Fields missed: " + str(errors)