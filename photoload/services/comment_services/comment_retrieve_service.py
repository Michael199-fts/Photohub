from django import forms
from service_objects.services import Service
from photoload.models import Comment


class GetCommentService(Service):
    pk = forms.IntegerField()
    validations = ['_checking_existing_comment', '_checking_missed_id']

    def process(self):
        self.result = self._comment
        return self

    @property
    def _comment(self):
        query = Comment.objects.get(id=self.cleaned_data.get('pk'))
        return query

    @property
    def _error_report(self):
        error_report = []
        if not self._checking_existing_comment():
            for validation in self.validations:
                if getattr(self, validation)():
                    error_report.append(getattr(self, validation)())
            return error_report
        else:
            error_report.append('Comment does not exist')
            return error_report

    def _checking_missed_id(self):
        if self.cleaned_data.get('pk') == '':
            return 'Id missed'

    def _checking_existing_post(self):
        try:
            Comment.objects.get(id=self.cleaned_data.get('pk'))
        except:
            return 'Comment does not exist'