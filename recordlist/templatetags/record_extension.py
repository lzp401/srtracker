__author__ = 'victorlu'

from django import template
from recordlist.support import UrlHelper


register = template.Library()


@register.filter
def field(value, arg):
    return getattr(value, arg)


@register.simple_tag
def page_url(param_str, page_number):
    param_str_new = UrlHelper.update_params(param_str, page=page_number)
    return UrlHelper.to_url(param_str_new)


@register.simple_tag
def sort_url(param_str, column_name, order=None):
    param_str_new = UrlHelper.update_params(param_str, col=column_name, order=order)
    return UrlHelper.to_url(param_str_new)


@register.simple_tag
def sr_url(sr_number):
    return 'http://internal-prod.vmware.com/casemgmt/srviewer/SRcaseDetails?srCaseNumber={0}'.format(sr_number)