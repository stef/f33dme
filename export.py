#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    export is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    export is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with export  If not, see <http://www.gnu.org/licenses/>.

# (C) 2012 by Stefan Marsiske, <stefan.marsiske@gmail.com>

import sys, os, opml

sys.path.append('/home/stf/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'f33dme.settings'

from django.conf import settings
from f33dme.models import Feed

for f in Feed.objects.all():
    print (u'%s\t%s' % (f.name, f.url)).encode('utf8')
