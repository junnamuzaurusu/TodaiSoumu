from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('captain-and-chief-officer/', views.captain_and_chief_officer, name='captain-and-chief-officer'),
    path('accounting/', views.accounting, name='accounting'),
]

