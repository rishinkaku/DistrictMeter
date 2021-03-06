# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'water'
urlpatterns = [
    
    url(r'^$', views.WaterListview.as_view(),name='home'),

    #数据监控
    url(r'station_monitor/',views.StaionMonitorView.as_view(),name='station_monitor'),
    url(r'dma_online/',views.DmaOnlineView.as_view(),name='dma_online'),
    url(r'rt_curve/',views.RTCurveView.as_view(),name='rt_curve'),
    url(r'big_user_online/',views.BigUserOnlineView.as_view(),name='big_user_online'),

    #数据分析 
    url(r'analy_usage/',views.AnalyUsageView.as_view(),name='analy_usage'),
    url(r'analy_flow_press/',views.AnalyFlowPressView.as_view(),name='analy_flow_press'),
    url(r'ajax/load_station',views.ajax_load_station,name='ajax_load_station'),

    #设备管理 
    url(r'flowmeter/',views.FlowMeterView.as_view(),name='flow_meter'),
]