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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Tag, Item
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import FeedForm
from datetime import datetime, timedelta


def index(request, paging=10):
    iall = Item.objects.all()
    item_num = len(iall)
    pag = Paginator(iall, paging)
    tags = Tag.objects.all()
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        items = pag.page(page)
    except (EmptyPage, InvalidPage):
        items = pag.page(1)
    form = FeedForm()
    return render_to_response('index.html', {'items': items, 'tags': tags, 'form': form})

def items_by_tag(request, tag_name):
    items = Item.objects.filter(tags__text__exact=tag_name)

    return render_to_response('items_by_tag.html', {'tag': tag_name, 'items': items})

def add_tag(request, tag_name):
    items = Item.objects.filter(tags__text__exact=tag_name)
    tag = Tag.objects.filter(text=tag_name)
    if not tag:
        tag = Tag(text=tag_name)
        tag.save()
        return HttpResponse('1')
    else:
        return HttpResponse('0')

def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(data=request.POST)
        if form.is_valid():
            event = form.save()
            return HttpResponse('OK')
            #return HttpResponseRedirect("%s" % post.get_nice_url())
    else:
        form = FeedForm()
    return HttpResponse('0')

