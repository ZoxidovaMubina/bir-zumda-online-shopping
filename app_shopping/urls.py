from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mahsulotlar', views.mahsulotlar, name='mahsulot'),
    path('/blog', views.blog, name='blog'),
    path('/mahsulotdetail/<int:pk>/', views.mahsulot_detail, name='mahsulot-detail'),
    path('/login', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('confirm_password/', views.confirm_password, name='confirm_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
