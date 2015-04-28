__author__ = 'victorlu'

from django import template
from django.http.request import QueryDict

import recordlist.constrant as constrant

register = template.Library()


@register.filter
def field(value, arg):
    return getattr(value, arg)


@register.filter
def dump_col_url(url, col):
    return _dump_url(url, col=str(col))


@register.filter
def dump_page_url(url, page):
    return _dump_url(url, page=str(page))


@register.filter
def dump_order_url(url, col):
    _dict = QueryDict(url.replace('?', ''), mutable=True)

    if _dict.has_key('col'):
        if _dict['col'] == col:
            _dict['order'] = constrant.ASC if not _dict.has_key('order') else (constrant.DESC if _dict['order'] == constrant.ASC else constrant.ASC)
        else:
            _dict.pop('order') if _dict.has_key('order') else None

    _dict['col'] = col

    return '?%s' % ('&'.join([key + '=' + val for key, val in _dict.iteritems()]))


def _dump_url(url, **kwargs):
    _dict = QueryDict(url, mutable=True)

    for key, val in kwargs.iteritems():
        _dict[key] = val

    return '?%s' % ('&'.join([key + '=' + val for key, val in _dict.iteritems()]))