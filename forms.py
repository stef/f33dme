from django import forms
from models import Feed, Tag
from datetime import datetime
from django.conf import settings

class BaseForm(forms.Form):
    def as_div(self):
        return self._html_output(u'<div class="form-row">%(field)s :%(label)s <div class="helper-text">%(help_text)s</div> %(errors)s</div>', u'<div class="form-row">%s</div>', u'</div>', u'%s', False)

class FeedForm(BaseForm):
    name = forms.CharField(label=u'Name', max_length=4096, required=True)
    url = forms.CharField(label=u'URL', required=True)
    tags = forms.CharField(label=u'Tags', max_length=4096, required=False)

    def save(self):
        new = Feed.objects.create(url = self.cleaned_data['url'],
                                  #tags = self.cleaned_data['tags'],
                                  name = self.cleaned_data['name'],
                                  )

        for tag in self.cleaned_data['tags'].split():
            try:
                t = Tag.objects.get(text=tag)
                new.tags.add(t)
            except:
                new.tags.create(text=tag)
        return new

