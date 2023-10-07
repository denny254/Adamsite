from django.urls import path
from .views import UserList, UserListWithID,RegisterAPI, LoginAPI, LogoutAPI
from knox import views as Knox_views
from .import views




urlpatterns = [
      #authentication  
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserListWithID.as_view(), name='user-list'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('logoutall/', Knox_views.LogoutAllView.as_view(), name='logoutall'),
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