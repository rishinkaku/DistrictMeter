from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import cookbook as cb

app_name = 'gis'
urlpatterns = [
    url(r'^$',views.index,name='index'),

    url(r'^(?P<page>.+\.html)$', views.StaticView.as_view()),
    url(r'^(?P<page>.+\.gml)$', views.StaticView.as_view()),
    url(r'^(?P<page>.+\.kml)$', views.StaticView.as_view()),
    url(r'^(?P<page>.+\.png)$', views.StaticView.as_view()),

    url(r'^getGeom',views.getGeom,name='getGeom'),
    url(r'^country/', TemplateView.as_view(template_name='gis/country.html')),
    url(r'^data/geojson/countries.geojson',views.countries,name='countries'),
    # url(r'^data/geojson/countries.geojson',TemplateView.as_view(template_name='data/geojson/countries.geojson')),

    url(r'^cookbook/$', TemplateView.as_view(template_name='gis/cookb/cookbook.html')),
    # url(r'^cookbook/ch01',cb.ch01,name='fullscreen'),
    url(r'^cookbook/ch01-map-controls/$',cb.ch01_map_controls,name='map_control'),
    url(r'^cookbook/ch01-moving-around/$',cb.ch01_moving_around,name='moving_around'),
    url(r'^cookbook/ch01-map-extent/$',TemplateView.as_view(template_name='gis/cookb/ch01_map_extent.html'),name='map_extent'),

    url(r'^cookbook/ch02-bing-maps/$',TemplateView.as_view(template_name='gis/cookb/ch02_bing_maps.html'),name='bing_maps'),
    url(r'^cookbook/ch02-openstreetmap/$',TemplateView.as_view(template_name='gis/cookb/ch02_openstreetmap.html'),name='openstreetmap'),
    url(r'^cookbook/ch02-wms-layers/$',TemplateView.as_view(template_name='gis/cookb/ch02_wms_layers.html'),name='wms_layers'),
    url(r'^cookbook/ch02-zoom-effect/$',TemplateView.as_view(template_name='gis/cookb/ch02_zoom_effect.html'),name='zoom_effect'),
    url(r'^cookbook/ch02-layer-opacity/$',TemplateView.as_view(template_name='gis/cookb/ch02_layer_opcity.html'),name='layer_opacity'),
    url(r'^cookbook/ch02-layer-preloading/$',TemplateView.as_view(template_name='gis/cookb/ch02_layer_preloading.html'),name='layer_preloading'),
    url(r'^cookbook/ch02-image-layer/$',TemplateView.as_view(template_name='gis/cookb/ch02_image_layer.html'),name='image_layer'),
    url(r'^cookbook/ch02-tile-size/$',TemplateView.as_view(template_name='gis/cookb/ch02_tile_size.html'),name='tile_size'),


    url(r'^cookbook/ch03-gml-layer/$',TemplateView.as_view(template_name='gis/cookb/ch03_gml_layer.html'),name='gml_layer'),
    url(r'^cookbook/ch03-kml-layer/$',TemplateView.as_view(template_name='gis/cookb/ch03_kml_layer.html'),name='kml_layer'),
    url(r'^cookbook/ch03-creating-features/$',TemplateView.as_view(template_name='gis/cookb/ch03_creating_features.html'),name='creating_features'),
    url(r'^cookbook/ch03-export-geojson/$',TemplateView.as_view(template_name='gis/cookb/ch03_export_geojson.html'),name='export_geojson'),
    url(r'^cookbook/ch03-wkt-format/$',TemplateView.as_view(template_name='gis/cookb/ch03_wkt_format.html'),name='wkt_format'),
    url(r'^cookbook/ch03-markers/$',TemplateView.as_view(template_name='gis/cookb/ch03_markers.html'),name='markers'),
    url(r'^cookbook/ch03-removing-cloning-feature-overlays/$',TemplateView.as_view(template_name='gis/cookb/ch03_rcf_overlay.html'),name='rcf_overlay'),


    url(r'^cookbook/map-layer', TemplateView.as_view(template_name='gis/cookb/map-layers.html')),
]