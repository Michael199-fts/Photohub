from django import forms
from service_objects.services import Service
from photoload.models import Post, Comment, User


class CreateCommentService(Service):
    post_id = forms.IntegerField(required=False)
    user_id = forms.IntegerField(required=False)
    target_comment = forms.IntegerField(required=False)
    text = forms.CharField(required=False)
    validations = ['_checking_missed_fields', '_checking_existing_post']

    def process(self):
        if not self._error_report:
            if self._nested_comment_check():
                self.result =  self._nested_commentary
                self.error_report = []
            else:
                self.result = self._commentary
                self.error_report = []
        else:
            self.error_report = self._error_report
        return self

    @property
    def _commentary(self):
        return Comment.objects.create(
            text=self.cleaned_data.get('text'),
            author=User.objects.get(id=self.cleaned_data.get('user_id')),
            target=Post.objects.get(id=self.cleaned_data.get('post_id')),
        )

    @property
    def _nested_commentary(self):
        return Comment.objects.create(
            text=self.cleaned_data.get('text'),
            author=User.objects.get(id=self.cleaned_data.get('user_id')),
            target=Post.objects.get(id=self.cleaned_data.get('post_id')),
            target_comment=Comment.objects.get(id=self.cleaned_data.get('target_comment'))
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

    def _nested_comment_check(self):
        if self.cleaned_data.get('target_comment'):
            return True
        else:
            return False