from django.urls import path
from . import views

urlpatterns = [
    path('echo', views.echo, name='echo'),
    path('getPrice', views.get_price, name='get_price'),
    path('compute', views.compute, name='compute'),
    path('parse', views.parse, name='parse'),
    path('query', views.query, name='query'),
]