from django import forms
from service_objects.services import Service
from photoload.models import Comment


class DeleteCommentService(Service):
    user_id = forms.IntegerField(required=False)
    pk = forms.IntegerField(required=False)
    validations = ['_checking_existing_comment', '_checking_missed_id', '_checking_author']

    def process(self):
        if not self._error_report:
            self._delete()
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    def _delete(self):
        instance = Comment.objects.get(id=self.cleaned_data.get('pk'))
        instance.delete()

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

    def _checking_author(self):
        instance = Comment.objects.get(id=self.cleaned_data.get('pk'))
        if instance.author.id != self.cleaned_data.get('user_id'):
            return 'You cannot delete this comment'

    def _checking_existing_comment(self):
        try:
            Comment.objects.get(id=self.cleaned_data.get('pk'))
        except:
            return 'Comment does not exist'