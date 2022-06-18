from django import forms
from service_objects.services import Service
from photoload.models import Post, Comment


class UpdateCommentService(Service):
    pk = forms.IntegerField(required=False)
    text = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    validations = ['_checking_existing_comment', '_checking_missed_id', '_checking_author']
    post_fields = ['text']

    def process(self):
        if not self._error_report:
            self.result = self._partial_update
            self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    @property
    def _partial_update(self):
        instance = Comment.objects.get(id=self.cleaned_data.get('pk'))
        instance.text = self.cleaned_data.get('text')
        instance.save()
        return instance

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
            return 'You cannot change this comment'

    def _checking_existing_comment(self):
        try:
            Comment.objects.get(id=self.cleaned_data.get('pk'))
        except:
            return 'Comment does not exist'