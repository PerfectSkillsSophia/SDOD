from django.urls import path
from accounts.views import * 


urlpatterns = [
    path('register/',registerPage,name='register'),
    path('login/',loginPage,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('staffLogin/',staffLogin,name='staffLogin'),
]
