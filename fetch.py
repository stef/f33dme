#!/usr/bin/env python2.6

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


import sys, os

sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'f33dme.settings'

from django.conf import settings
from f33dme.models import Item, Feed
from feedparser import parse
from datetime import datetime

if __name__ == '__main__':
    feeds = Feed.objects.all()
    for feed in feeds:
        f = parse(feed.url)
        if not f:
            continue
        d = feed.updated
        for item in reversed(f['entries']):
            tmp_date = datetime(*item['updated_parsed'][:6])
            if tmp_date < feed.updated:
                continue
            if tmp_date > d:
                d = tmp_date
            # title content updated
            c = unicode(item.content[0].value)
            t = unicode(item['title'])
            u = item['links'][0]['href']
            # date as tmp_date?!
            new_item = Item(url=u, title=t, content=c, feed=feed, date=tmp_date)
            new_item.save()
        feed.updated = d
        feed.save()
