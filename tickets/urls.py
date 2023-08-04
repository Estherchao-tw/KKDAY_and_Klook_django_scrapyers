from django.urls import path
from . import views

app_name = "tickets"
 
urlpatterns = [
    # path('', views.home, name="home"),
    path('',views.index, name='index')
]