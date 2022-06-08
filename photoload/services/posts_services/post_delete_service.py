from django import forms
from service_objects.services import Service
from photoload.models import Post, User


class DeletePostService(Service):
    user_id = forms.IntegerField(initial=None, required=False)
    id = forms.IntegerField(initial=None, required=False)
    validations = ['_checking_missed_id', '_checking_author']

    def process(self):
        import pdb
        pdb.set_trace()
        if not self._error_report:
            self._delete()
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    def _delete(self):
        instance = Post.objects.get(id=self.cleaned_data.get('id'))
        instance.delete()

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
            return 'You cannot delete this post'