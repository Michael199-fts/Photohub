from django import forms
from service_objects.services import Service
from photoload.models import Comment, Post


class GetCommentListService(Service):
    sort_by = forms.CharField(required=False)
    filter_by = forms.CharField(required=False)
    filter_value = forms.CharField(required=False)
    pk = forms.CharField(required=False)
    sorting_values = ['upload_date', '-upload_date', 'author_username', '-author_username']
    filter_values = ['author_id', 'author_username', 'upload_date']


    def process(self):
        self.result = self._comment
        return self

    @property
    def _comment(self):
        query = Comment.objects.all().filter(target = Post.objects.get(id=self.cleaned_data.get('pk')))
        if self.cleaned_data.get('filter_by'):
            if self.cleaned_data.get('filter_by') in self.filter_values:
                if self.cleaned_data.get('filter_value'):
                    query = query.filter(**{self.cleaned_data.get('filter_by'):self.cleaned_data.get('filter_value')})
        if self.cleaned_data.get('sort_by'):
            if self.cleaned_data.get('sort_by') in self.sorting_values:
                query = query.order_by(self.cleaned_data.get('sort_by'))
        return query
