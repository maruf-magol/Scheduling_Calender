from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_details, name='task_details'),  # Task details

]