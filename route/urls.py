from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='type'),
    path('map',views.map, name='map'),
    # path('show_map',views.map, name='show_map'),
]