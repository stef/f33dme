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

from django.conf.urls.defaults import patterns, include
from django.conf import settings
import views as view
from django.contrib import admin

admin.autodiscover()

root_url = r'^'

urlpatterns = patterns('',
    (r'^$', view.index),
    (r'^tag/(?P<tag_name>.*)$', view.items_by_tag),
    (r'^add_tag/(?P<tag_name>.*)$', view.add_tag),
    (r'^add_feed$', view.add_feed),
    (r'^archive/(?P<item_id>.*)$', view.archive),
    (r'^bulk_archive/(?P<page_id>.*)$', view.bulk_archive),
    (r'^opml_import/(?P<url>.*)$', view.opml_import),
    (root_url+'admin/', include(admin.site.urls)),
    #(root_url+'admin/', include(admin.site.urls)),
)

if settings.DEV_SERVER:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PATH}),
    )
