from django import forms
from service_objects.services import Service
from photoload.models import User, Rate, Post


class CreateRateService(Service):
    value = forms.IntegerField(required=False)
    user_id = forms.IntegerField(required=False)
    post_id = forms.CharField(required=False)
    validations = ['_checking_missed_fields', '_checking_existing_post', '_checking_existing_rate']

    def process(self):
        if not self._error_report:
            self.result = self._rate
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    @property
    def _rate(self):
        instance = Post.objects.get(id=self.cleaned_data.get('post_id'))
        instance.rating += self.cleaned_data.get('value')
        instance.save()
        return Rate.objects.create(
            value=self.cleaned_data.get('value'),
            author=User.objects.get(id=self.cleaned_data.get('user_id')),
            target_post=Post.objects.get(id=self.cleaned_data.get('post_id')),
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

    def _checking_existing_post(self):
        try:
            Post.objects.get(id=self.cleaned_data.get('post_id'))
        except:
            return 'Post does not exist'

    def _checking_existing_rate(self):
        try:
            Rate.objects.get(author=self.cleaned_data.get('user_id'), target_post=self.cleaned_data.get('post_id'))
            return "Оценка уже поставлена"
        except:
            pass