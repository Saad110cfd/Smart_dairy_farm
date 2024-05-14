from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'dairymanagementsystem'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),   
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('farm_detail/', views.farm_detail, name='farm_detail'),
    path('add_farm/', views.add_farm, name='add_farm'),
    path('edit_farm/', views.edit_farm, name='edit_farm'),
    path('edit_farm_detail/<int:farm_id>/', views.edit_farm_detail, name='edit_farm_detail'),
    path('delete_farm/', views.delete_farm, name='delete_farm'),
    path('animal_add/', views.animal_add, name='animal_add'),
    path('animal_details/', views.animal_details, name='animal_details'),
    path('edit_animal/', views.edit_animal, name='edit_animal'),
    path('edit_animal_details/<str:animal_name>/', views.edit_animal_details, name='edit_animal_details'),
    path('delete_animal/', views.delete_animal, name='delete_animal'),
    path('add_milk_production', views.add_milk_production, name = 'add_milk_production'),
    path('milk_detail', views.milk_detail, name = 'milk_detail')

]
