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
from models import Tag, Item, Feed
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import FeedForm
from django.conf import settings
import opml
from django.db.models import Q


def index(request):
    paging = settings.PAGING
    iall = Item.objects.filter(archived=False).all()
    item_num = len(iall)
    pag = Paginator(iall, paging)
    tags = Tag.objects.all()
    page = int(request.GET.get('page', '1'))
    try:
        items = pag.page(page)
    except (EmptyPage, InvalidPage):
        items = pag.page(1)
    form = FeedForm()
    return render_to_response('index.html', {'items': items, 'tags': tags, 'form': form, 'item_num': item_num, 'page_num': page})

def feed_view(request, id):
    paging = settings.PAGING
    iall = Item.objects.filter(feed__id=id).all()
    item_num = len(iall)
    pag = Paginator(iall, paging)
    tags = Tag.objects.all()
    page = int(request.GET.get('page', '1'))
    try:
        items = pag.page(page)
    except (EmptyPage, InvalidPage):
        items = pag.page(1)
    form = FeedForm()
    return render_to_response('index.html', {'items': items, 'tags': tags, 'form': form, 'item_num': item_num, 'page_num': page, 'msg': 'F33d "%s"' % Feed.objects.filter(id=id).all()[0].name})

def search(request):
    q = request.GET.get('q')
    if not q:
        return HttpResponse('no search strings found')
    paging = settings.PAGING
    iall = Item.objects.filter(Q(content__contains=q) | Q(title__contains=q)).all()
    item_num = len(iall)
    pag = Paginator(iall, paging)
    tags = Tag.objects.all()
    page = int(request.GET.get('page', '1'))
    try:
        items = pag.page(page)
    except (EmptyPage, InvalidPage):
        items = pag.page(1)
    form = FeedForm()
    return render_to_response('index.html', {'items': items, 'tags': tags, 'form': form, 'item_num': item_num, 'page_num': page, 'msg': 'Search result for "%s"' % q, 'q': q})

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

def archive(request, item_id):
    item = Item.objects.get(id=item_id)
    if not item:
        return HttpResponse('No item found')
    item.archived = True
    item.save()
    return HttpResponse('OK')

def bulk_archive(request, page_id):
    paging = settings.PAGING
    iall = Item.objects.filter(archived=False).all()
    item_num = len(iall)
    pag = Paginator(iall, paging)
    tags = Tag.objects.all()
    page = int(request.GET.get('page', '1'))
    try:
        items = pag.page(page)
    except:
        return HttpResponse('Page not found')
    for item in items.object_list:
        item.archived = True
        item.save()
    return HttpResponse('OK')

def opml_import(request, url):
    try:
        o = opml.parse(url)
    except:
        return HttpResponse('Cannot parse opml file %s' % url)
    for f in o:
        new = Feed.objects.create(url = f.xmlUrl,
                                  #tags = self.cleaned_data['tags'],
                                  name = f.title,
                                  )
        new.save()
    return HttpResponse('OK')
