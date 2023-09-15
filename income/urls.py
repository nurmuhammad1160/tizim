from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='incomeHome'),
    path('base/',views.base,name='base'),
    path('searchProduct/',views.search,name='searchProduct'),
    path('sell/',views.sellProduct,name='sellProduct'),
    path('sotish/',views.sotish,name='sotish'),
    path('income/delete/<int:product_id>/', views.delete_amount, name='delete_amount'),
]