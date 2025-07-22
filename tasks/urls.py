from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.taskList, name='tasks'),
    path('create/', views.taskCreate, name='task-create'),
    path('update/<int:pk>/', views.taskUpdate, name='task-update'),
    path('delete/<int:pk>/', views.taskDelete, name='task-delete'),
]