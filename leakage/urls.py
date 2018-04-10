"""leakage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,handler404,handler500
from django.contrib import admin

from dma.views import i18n_javascript,home,main,test,HomeView,JoinFormView,error_404,error_500
from django.views.generic import TemplateView
from water.views import WaterListview
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^admin/jsi18n', i18n_javascript),
    url(r'^admin/', admin.site.urls),
    # url(r'^$',home,name='home'),
    url(r'^$',TemplateView.as_view(template_name='virvo/home.html'),name='home'),
    url(r'^main/', main,name='main'),
    url(r'^test/(?P<var>\d+)/$', test,name='test'),

    url(r'^join/', JoinFormView.as_view()),

    #dma
    url(r'^dma/', include('dma.urls', namespace='dma')),
    #map
    url(r'^gis/', include('gis.urls', namespace='gis')),

     #water
    url(r'^water/', include('water.urls', namespace='water')),

    #virvo
    url(r'^virvo/', include('virvo.urls', namespace='virvo')),


]

handler404 = error_404
handler500 = error_500