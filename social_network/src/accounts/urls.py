from django.urls import path 
from .views import RegisterView, LoginView,Logout


app_name = 'accounts'
urlpatterns = [
    path('register/',RegisterView.as_view(),name='accounts-register'),
    path('login/',LoginView.as_view(),name='accounts-login'),
    path('logout/',Logout.as_view(),name = 'accounts-logout'),
    
]
