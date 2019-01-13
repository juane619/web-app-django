from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import *

from django.urls import path

urlpatterns = [
    url(r'^home/', HomePageView.as_view(), name='index'),

    url(r'^restaurants/new/$', RestaurantCreateView.as_view(), name='rest_insert'),
    url(r'^restaurants/search/$',
        TemplateView.as_view(template_name='restaurants/find_rest.html'), name='rest_find'),
    url(r'^restaurants/list/$', RestListView.as_view(), name='rest_found'),
    url(r'busqueda_restaurantes/$', busqueda_restaurantes,
        name='busqueda_restaurantes'),

    url(r'^restaurants/update/(?P<pk>\d+)/$',
        RestEditView.as_view(), name='rest_edit'),
    url(r'^restaurants/delete/(?P<pk>\d+)/$',
        RestDeleteView.as_view(), name='rest_delete'),
    url(r'^restaurants/map/(?P<lon>-?\d+.?\d+)/(?P<lat>-?\d+.?\d+) /$',
        MapRestaurantView.as_view(), name='rest_map'),

    url(r'^dish/new/$', DishCreateView.as_view(), name='dish_insert'),
    url(r'^dish/list/$', DishListView.as_view(), name='dish_list'),
    url(r'^dish/update/(?P<pk>\d+)/$', DishEditView.as_view(), name='dish_edit'),
    url(r'^dish/delete/(?P<pk>\d+)/$',
        DishDeleteView.as_view(), name='dish_delete'),

    url(r'^graphics/$', ChartView.as_view(), name='graphics'),
    url(r'view_chart/$', getRestByDistricts,
        name='view_chart'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r"^account/(?P<slug>[\w-]+)/$",
        UserDetailView.as_view(), name="user_detail"),
    # debemos crear formulario de creacion, vision/modificacion de usuario como modelo
    # y una vez echo esto, crear lo mismo para restaurantes.
]
