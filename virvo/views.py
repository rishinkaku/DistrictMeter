# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages
from . models import Organization,Stations,DMABaseinfo,Alarms
import json
import random
from datetime import datetime

from mptt.utils import get_cached_trees
from mptt.templatetags.mptt_tags import cache_tree_children

from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .tables import StationsTable
from django_tables2 import RequestConfig

from django.urls import reverse_lazy
from .forms import DMABaseinfoForm,CreateDMAForm,TestForm,StationsCreateManagerForm,StationsForm

import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
# from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin




# from dma.fusioncharts import FusionCharts


# from .fusioncharts import FusionCharts

# Create your views here.


def recursive_node_to_dict(node,url_cat):
    result = {
        'id':node.pk,
        'name': node.name,
        'open':'true',
        'url':'/virvo/dma/{}/{}'.format(node.pk,url_cat),
        'target':'_self',
        'icon':"/static/virvo/images/站点管理/u842_1.png",
    }
    
    children = [recursive_node_to_dict(c,url_cat) for c in node.get_children()]
    
    # get each node's station if exist
    # try:
    #     sats = node.station.all()
    #     for s in sats:
    #         children.append({'name':s.station_name})
    #     # children.append({'name':})
    # except:
    #     pass

    if children:
        result['children'] = children
    
    return result

def get_stationtree(request):
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,'station'))

    
    # print json.dumps(dicts, indent=4)

    
    
    return JsonResponse({'trees':dicts})


def get_dmatree(request):
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,''))

    
    # print json.dumps(dicts, indent=4)

    
    
    return JsonResponse({'trees':dicts})

def gettree(request):
    print(request.GET)
    page_name = request.GET.get('page_name') or ''
    print(page_name)
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,page_name))

    
    # print json.dumps(dicts, indent=4)

    
    
    return JsonResponse({'trees':dicts})

def gettreenode(request):
    node = request.POST['node']
    
    orgs = Organization.objects.filter(name=node).first()
    
    table = StationsTable(Stations.objects.filter(belongto=orgs))
    
    # table = StationsTable(orgs.station_set.all())
    
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    vals = {'table':table}
    return render(request,'virvo/table_station.html',vals)
    # return JsonResponse(vals)    

def getchartd(request):
    data = [random.randint(2,13), 20, 6, 10, 20, 30]

    return JsonResponse({'data':data})  

class rt_curveView(TemplateView):
    """docstring for rt_curveView"""
    template_name = 'virvo/rt_curve.html'

    def get_context_data(self, *args, **kwargs):
        context = super(rt_curveView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '实时曲线'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        stations_list = Stations.objects.filter(belongto=orgs)
        context['station_list'] = stations_list

        for station in stations_list:
            pass

        rt_dataset = []
        def curse_data(s):
            result = {
                'chart_id':'chart_{}'.format(s.station_name),
                'data':[1,2,3,4,5,6],
                'station_name':s.station_name,
                'caliber':s.caliber
            }
            return result

        jsd=[]
        for s in stations_list:
            rt_dataset.append(curse_data(s) )
            jsd.append({'data':[random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13)],
                'name':'chart_{}'.format(s.station_name)})
        
        context['rt_dataset'] = rt_dataset
        dum=json.dumps(jsd)
        # print(type(dum),dum)

        data = [random.randint(2,13), 20, 6, 10, 20, 30]
        context['jsd'] = json.dumps(jsd)

        

        return context
        

class rt_dataView(TemplateView):
    """docstring for rt_curveView"""
    template_name = 'virvo/rt_data.html'

    def get_context_data(self, *args, **kwargs):
        context = super(rt_dataView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '实时数据'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        stations_list = Stations.objects.filter(belongto=orgs)
        context['stations_list'] = stations_list

        

        return context

class MNFView(TemplateView):
    """docstring for StationsView"""

    
    template_name = 'virvo/mnf.html'
    
    def get_context_data(self, *args, **kwargs):
        
        context = super(MNFView, self).get_context_data(*args, **kwargs)

        
        # if self.request.method == 'POST':
        #     form = AnalyWaterForm(self.request.POST or None)
        # else:
            
        #     form = AnalyWaterForm()
            
        # context['form'] = form

        # table = StationsTable(Stations.objects.all())
        # RequestConfig(self.request, paginate={'per_page': 10}).configure(table)
        # context['table'] = table

        
                
        return context                 


class AjaxTemplateMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class TestFormView(SuccessMessageMixin, AjaxTemplateMixin, FormView):
    template_name = 'virvo/test_form.html'
    form_class = TestForm
    success_url = reverse_lazy('home')
    success_message = "Way to go!"        



def create_dma(request):
    
    print(request.POST)
    if request.method == 'POST':
        # dma_no = request.POST.get('dma_no')
        # dma_name = request.POST.get('dma_name')
        # creator = request.POST.get('creator')
        create_date = request.POST.get('create_date')
        print(create_date)
    dma_form = CreateDMAForm(request.POST or None)
    if dma_form.is_valid():
        parent = Organization.objects.first()
        orgs = Organization.objects.create(name=dma_form.cleaned_data.get('dma_name'),parent=parent)

        obj = DMABaseinfo.objects.create(dma_no=dma_form.cleaned_data.get('dma_no'),dma=orgs)
        # return HttpResponseRedirect("/virvo/dma/1/")
    if dma_form.errors:
        print(dma_form.errors)
    return render(request,'virvo/dma_manager.html',{'dma_form':dma_form})

class DMAListView(UpdateView):
    template_name = 'virvo/dma_manager.html'
    form_class = DMABaseinfoForm
    model = DMABaseinfo
    # success_url = '/virvo/dma/1'

    def get_queryset(self):
        return DMABaseinfo.objects.all()

    def get_form_kwargs(self):
        print (self.kwargs)
        kwargs = super(DMAListView, self).get_form_kwargs()
        # kwargs['user'] = self.request.user
        print (kwargs)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(DMAListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'DMA 管理'
        pk = self.kwargs.get('pk')
        orgs = Organization.objects.get(pk=pk)
        context['station_list'] = Stations.objects.filter(belongto=orgs)

        create_dma_form = CreateDMAForm()
        context['dma_form'] = create_dma_form

        return context

    def form_valid(self,form):
        orgs = form.cleaned_data.get('orgs')
        print(orgs,type(orgs))
        print (form.instance)
        print(form.instance.dma)
        # print(form.instance.dma.parent)
        form.instance.dma.parent = orgs
        form.instance.dma.save()

        return super(DMAListView,self).form_valid(form)





"""
Stations creation, manager
"""
class StationsCreateMangerView(CreateView):
    model = Stations
    template_name = 'virvo/stations_create_manager.html'
    form_class = StationsCreateManagerForm
    # success_url = reverse_lazy('stations_list_manager');

    # @method_decorator(permission_required('virvo.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(StationsCreateMangerView, self).dispatch(*args, **kwargs)


"""
Stationss list, manager
"""
class StationsListMangerView(ListView):
    model = Stations
    template_name = 'virvo/stations_list_manager.html'

    # @method_decorator(permission_required('virvo.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(StationsListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # user = self.request.user
        # manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
        # if manager_group in user.groups.all():
        #     manager = Manager.objects.get(user=user)
        #     return Stations.objects.filter(centre__in=manager.centres.all())
        # else:
        #     return Stations.objects.all()
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        # print(pk,orgs)
        return Stations.objects.filter(belongto=orgs)

    def get_context_data(self,**kwargs):
        context = super(StationsListMangerView,self).get_context_data(**kwargs)

        return context


"""
Stations edit, manager
"""
class StationsUpdateManagerView(UpdateView):
    model = Stations
    form_class = StationsForm
    template_name = 'virvo/stations_edit_manager.html'

    # @method_decorator(permission_required('virvo.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.stations_id = kwargs['pk']
        return super(StationsUpdateManagerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        stations = Stations.objects.get(id=self.stations_id)
        return HttpResponse(render_to_string('virvo/stations_edit_manager_success.html', {'stations': stations}))

    def get_context_data(self, **kwargs):
        context = super(StationsUpdateManagerView, self).get_context_data(**kwargs)
        context['page_title'] = '修改站点'
        return context


class StationsAlarmView(DetailView):
    """docstring for StationsAlarmView"""
    template_name = 'virvo/alarminfo.html'


    def get_queryset(self):
        pk = self.kwargs.get('pk')

        return Alarms.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(StationsAlarmView, self).get_context_data(**kwargs)
        context['page_title'] = '报警信息'

        pk = self.kwargs.get('pk')
        print(pk)

        qs = Stations.objects.get(id=pk)

        context['qs'] = qs.alarms_set.all()
        return context



class DailyuseView(TemplateView):
    """docstring for DailyuseView"""
    template_name = 'virvo/daily_use.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DailyuseView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '日用水分析'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        stations_list = Stations.objects.filter(belongto=orgs)
        context['station_list'] = stations_list

        for station in stations_list:
            pass

        rt_dataset = []
        def curse_data(s):
            result = {
                'chart_id':'chart_{}'.format(s.station_name),
                'data':[1,2,3,4,5,6],
                'station_name':s.station_name,
                'caliber':s.caliber
            }
            return result

        jsd=[]
        for s in stations_list:
            rt_dataset.append(curse_data(s) )
            jsd.append({'data':[random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13)],
                'name':'chart_{}'.format(s.station_name)})
        
        context['rt_dataset'] = rt_dataset
        dum=json.dumps(jsd)
        # print(type(dum),dum)

        data = [random.randint(2,13), 20, 6, 10, 20, 30]
        context['jsd'] = json.dumps(jsd)

        

        return context        