from django import forms
from service_objects.services import Service
from photoload.models import Post


class UpdatePostService(Service):
    id = forms.IntegerField(initial=None, required=False)
    title = forms.CharField(initial=None, required=False)
    text = forms.CharField(initial=None, required=False)
    photo = forms.ImageField(initial=None, required=False)
    user_id = forms.IntegerField(initial=None, required=False)
    validations = ['_checking_missed_id', '_checking_author']
    post_fields = ['title', 'text', 'photo']

    def process(self):
        if not self._error_report:
            self.result = self._partial_update
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    @property
    def _partial_update(self):
        instance = Post.objects.get(id=self.cleaned_data.get('id'))
        update_fields = []
        for el, val in self.cleaned_data.items():
            if el == 'id' or el == 'user_id':
                continue
            else:
                if el in self.post_fields:
                    if val != '':
                        setattr(instance, el, val)
                        update_fields.append(el)
        instance.save(update_fields=update_fields)
        return instance

    @property
    def _error_report(self):
        error_report = []
        for validation in self.validations:
            if getattr(self, validation)():
                error_report.append(getattr(self, validation)())
        return error_report


    def _checking_missed_id(self):
        if self.cleaned_data.get('id') == '':
            return 'Id missed'


    def _checking_author(self):
        instance = Post.objects.get(id=self.cleaned_data.get('id'))
        if instance.author.id != self.cleaned_data.get('user_id'):
            return 'You cannot change this post'