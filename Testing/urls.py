from django.urls import path

from TestApp import views

urlpatterns = [
    path('', views.home),
    path('add_user/', views.AddUser.as_view()),
    path('add_friend/', views.AssignFriends.as_view())
]
