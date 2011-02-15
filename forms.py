# This file is part of f33dme.
#
#  f33dme is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  f33dme is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with f33dme.  If not, see <http://www.gnu.org/licenses/>.
#
# (C) 2011- by Adam Tauber, <asciimoo@gmail.com>

from django import forms
from models import Feed
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
        return new

