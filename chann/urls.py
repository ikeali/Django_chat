# from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='chann/login.html'), name='login'),
    path('signin/', views.signin, name='signin'),  # Add this line for the login view
    path('signout/',views.signout,name='signout'),

]
