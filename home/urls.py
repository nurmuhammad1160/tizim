from django.urls import path
from . import views



urlpatterns = [
    path('', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.sign_out, name='logout'),
    path('barcha/', views.barcha, name='barcha'),
    path('statistica/', views.statistica, name='statistica'),
    path('delete/<int:p_id>', views.deleteProduct, name='delete'),
    path('edit/<int:p_id>/', views.editProduct, name='edit'),
    path('createProduct/', views.createProduct, name='createProduct'),
    path('view/<int:p_id>/', views.detailProduct, name='detail'),
    path('productSearch/', views.productSearch, name='productSearch'),
    path('register', views.register, name='register'),
]