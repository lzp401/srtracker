from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Record
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
import datetime
import constraint
from recordlist.constraint import FilterType
from support import ColumnHeader, UrlHelper, RecordDescriptor, FilterHelper


# Create your views here.
def index(request):
    template = loader.get_template("recordlist/index.html")

    list_display = ('srNumber', 'customer', 'openDate', 'calPriority', 'modifiedDate', 'touchDate', 'reviewRequired', 'description', )

    order_column = request.GET.get('col') if request.GET.has_key('col') else 'modifiedDate'
    order = request.GET.get('order') if request.GET.has_key('order') else constraint.DESC

    filter_dict = None

    if request.POST.has_key('clean-filter'):
        FilterHelper.saved_dict = None
        filter_enabled = 'off'
    else:
        filter_enabled = request.GET.get('filter') if request.GET.has_key('filter') else 'off'

    if filter_enabled == 'on':
        if request.POST.has_key('save-filter'):
            filter_dict = FilterHelper.format_filter_dict(request.POST) if filter_enabled == 'on' else None
            FilterHelper.saved_dict = filter_dict
        else:
            filter_dict = FilterHelper.saved_dict

    if filter_enabled == 'on' and filter_dict:
        records_all = Record.objects.filter(**filter_dict).order_by(('-' if order == constraint.DESC else '') + order_column)
    else:
        records_all = Record.objects.order_by(('-' if order == constraint.DESC else '') + order_column)

    pagesize = request.GET.get('pagesize') if request.GET.has_key('pagesize') else 50
    page = request.GET.get('page') if request.GET.has_key('page') else 1
    paginator = Paginator(records_all, pagesize)

    records = paginator.page(page)

    current_param_str = UrlHelper.format_params(request.GET)

    column_headers = [ColumnHeader(name, UrlHelper.update_params(current_param_str, col=name)) for name in list_display]

    for header in column_headers:
        header.show_caret = header.name == order_column
        header.caret_style = '' if order == constraint.DESC and header.show_caret else 'dropup'

        if header.show_caret:
            header.order = constraint.DESC if order == constraint.ASC else constraint.ASC


    if filter_dict:
        filter_dict = FilterHelper.filter_dict_description(filter_dict)

    context = RequestContext(request, {
        'header_all': column_headers,
        'records': records,
        'header_no_id': list_display,
        'total_count': records_all.count(),
        'current_url': current_param_str,
        'filter_config': RecordDescriptor().descriptor,
        'filter_type': FilterType,
        'filter_detail': filter_dict
    })

    return HttpResponse(template.render(context))


def detail(request, recordid):
    template = loader.get_template("recordlist/detail.html")

    record = Record.objects.get(recordId=recordid)

    readonly_fields = ('recordId', 'srNumber', 'customer', 'description', 'openDate', 'modifiedDate',
                       'touchDate', 'closeDate',)
    editable_fields = ('calReviewDate', 'calSummary', 'overallStatus',
                       'calPriority', 'faultCategory', 'reviewRequired', 'escalationLevel')

    context = RequestContext(request, {
        'record': record,
        'readonly_fields': readonly_fields,
        'editable_fields': editable_fields,
        'review_enabled': '' if record.reviewRequired else 'disabled="disabled"',
    })

    return HttpResponse(template.render(context))


def update(request, recordid):
    record = get_object_or_404(Record, recordId=recordid)

    action = {
        'review': request.POST.has_key('markReview'),
        'save': request.POST.has_key('save'),
    }

    record.calSummary = request.POST['calSummary']
    record.overallStatus = request.POST['overallStatus']
    record.calPriority = request.POST['calPriority']
    record.faultCategory = request.POST['faultCategory']
    record.escalationLevel = request.POST['escalationLevel']

    if action['review']:
        record.reviewRequired = False
        record.calReviewDate = datetime.date.today()
    else:
        record.reviewRequired = True

    record.save()

    if action['review']:
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('detail', args=(record.recordId,)))


def create(request):
    record = Record()

    action = request.POST.has_key('create')

    if action:
        record = Record.objects.create(
            calSummary=request.POST['calSummary'],
            overallStatus=request.POST['overallStatus'],
            calPriority=request.POST['calPriority'],
            faultCategory=request.POST['faultCategory'],
            reviewRequired=True
        )

        return HttpResponseRedirect(reverse('detail', args=(record.recordId,)))

    template = loader.get_template('recordlist/create.html')
    context = RequestContext(request, {
        'record': record,
    })

    return HttpResponse(template.render(context))


def markreview(request):
    recordids = request.POST.getlist('recordid')

    if len(recordids) > 0:
        records = Record.objects.filter(recordId__in=recordids)

        for record in records:
            record.reviewRequired = False
            record.calReviewDate = datetime.date.today()
            record.save()

    return HttpResponseRedirect(reverse('index'))

