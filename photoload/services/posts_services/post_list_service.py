from django import forms
from service_objects.services import Service
from photoload.models import Post


class GetPostListService(Service):
    sort_by = forms.CharField(initial=None, required=False)
    filter_by = forms.CharField(initial=None, required=False)
    filter_value = forms.CharField(initial=None, required=False)
    sorting_values = ['title', '-title', 'upload_date', '-upload_date', 'rating', '-rating']
    filter_values = ['title', 'author_id', 'author_username', 'upload_date', 'rating']


    def process(self):
        self.result = self._post
        return self

    @property
    def _post(self):
        query = Post.objects.all()
        if self.cleaned_data.get('filter_by') != []:
            if self.cleaned_data.get('filter_by') in self.filter_values:
                if self.cleaned_data.get('filter_value'):
                    query = query.filter(**{self.cleaned_data.get('filter_by'):self.cleaned_data.get('filter_value')})
        if self.cleaned_data.get('sort_by'):
            if self.cleaned_data.get('sort_by') in self.sorting_values:
                query = query.order_by(self.cleaned_data.get('sort_by'))
        return query
