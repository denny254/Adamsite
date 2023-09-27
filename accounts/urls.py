from django.urls import path
from .views import UserList,RegisterAPI, LoginAPI, LogoutAPI
from knox import views as Knox_views
from .import views



urlpatterns = [
    path('api/users/<int:pk>/', UserList.as_view(), name='user-list'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/register/', RegisterAPI.as_view(), name='register'),

    path('api/logout/', LogoutAPI.as_view(), name='logout'),
    path('api/logoutall/', Knox_views.LogoutAllView.as_view(), name='logoutall'),

    #writer 
     path('api/writers/', views.create_writer, name='create_writer'),
     path('api/writers/all/', views.get_all_writers, name='get_all_writers'),
     path('api/writers/<int:writer_id>/', views.get_writer, name='get_writer'),
     path('api/writers/update/<int:writer_id>/', views.update_writer, name='update_writer'),
     path('api/writers/delete/<int:writer_id>/', views.delete_writer, name='delete_writer'),
]