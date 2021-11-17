from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:brewcategory_slug>/<slug:brewproduct_slug>/', views.brewproduct, name='brewproduct'),
    path('<slug:brewcategory_slug>/', views.brewcategory, name='brewcategory')
]