from django.urls import path
from .import views
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    #authentiaction 
    path('auth/register/', views.CreateUserAPI.as_view()),
    path('auth/all-users/', views.ListUsersAPI.as_view()),
    path('auth/update-user/<int:pk>/', views.UpdateUserAPI.as_view()),
    path('auth/login/', views.LoginAPIView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/logout-all/', LogoutAllView.as_view()),

        #writers
    path('writers/', views.create_writer, name='create_writer'),
    path('writers/all/', views.get_all_writers, name='get_all_writers'),
    path('writers/<int:writer_id>/', views.get_writer, name='get_writer'),
    path('writers/update/<int:writer_id>/', views.update_writer, name='update_writer'),
    path('writers/delete/<int:writer_id>/', views.delete_writer, name='delete_writer'),

        #tasks
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'), 

        #projects 
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
]