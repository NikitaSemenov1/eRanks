from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event-management/', views.event_management, name="event-management"),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('student_signup/', views.student_signup_page, name='student_signup'),
    path('employer_signup/', views.employer_signup_page, name='employer_signup'),
    path('ranking/', views.ranking_page, name='ranking'),
    path('upload_file/', views.upload_file, name='upload_file')
]
