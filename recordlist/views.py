from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Record
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
import datetime
from templatetags import RecordFilter
import constrant

# Create your views here.


def index(request):
    template = loader.get_template("recordlist/index.html")

    list_display = ('recordId', 'srNumber', 'customer', 'openDate', 'calPriority', 'reviewRequired', 'description', )

    order_column = request.GET.get('col') if request.GET.has_key('col') else 'recordId'
    order = request.GET.get('order') if request.GET.has_key('order') else constrant.DESC

    records_all = Record.objects.order_by(('-' if order == constrant.DESC else '') + order_column)

    pagesize = request.GET.get('pagesize') if request.GET.has_key('pagesize') else 50
    page = request.GET.get('page') if request.GET.has_key('page') else 1

    paginator = Paginator(records_all, pagesize)

    records = paginator.page(page)

    url_formattre = lambda querydict: '&'.join([_key + '=' + _val for _key, _val in querydict.iteritems()])

    current_url = url_formattre(request.GET)

    class col_header:
        def __init__(self, name, link):
            self.name = name
            self.link = link
            self.show_caret = False
            self.caret_style = ''

        def __str__(self):
            return self.name

    column_headers = [col_header(col, RecordFilter.dump_col_url(current_url, col)) for col in list_display]

    for header in column_headers:
        header.show_caret = header.name == order_column
        header.caret_style = '' if order == constrant.DESC and header.show_caret else 'dropup'

    context = RequestContext(request, {
        'header_all': column_headers,
        'records': records,
        'header_no_id': list_display[1:],
        'total_count': records_all.count(),
        'current_url': current_url,
    })

    return HttpResponse(template.render(context))


def detail(request, recordid):
    template = loader.get_template("recordlist/detail.html")

    record = Record.objects.get(recordId=recordid)

    readonly_fields = ('recordId', 'srNumber', 'customer', 'description', 'openDate', 'modifiedDate',
                       'touchDate', 'closeDate', 'escalationLevel')
    editable_fields = ('calReviewDate', 'calSummary', 'overallStatus',
                       'calPriority', 'faultCategory', 'reviewRequired')

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

    if action['save']:
        record.calSummary = request.POST['calSummary']
        record.overallStatus = request.POST['overallStatus']
        record.calPriority = request.POST['calPriority']
        record.faultCategory = request.POST['faultCategory']

    if action['review']:
        record.reviewRequired = False
        record.calReviewDate = datetime.date.today()
    else:
        record.reviewRequired = True

    record.save()

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

