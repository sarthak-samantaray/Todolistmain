from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',views.TaskList.as_view(),name='TaskList'),
    path('task/<int:pk>',views.TaskDetail.as_view(),name='TaskDetail'),
    path('taskcreate/',views.TaskCreate.as_view(),name='TaskCreate'),
    path('taskupdate/<int:pk>',views.TaskUpdate.as_view(),name='TaskUpdate'),
    path('taskdelete/<int:pk>',views.TaskDelete.as_view(),name='TaskDelete'),
    path('login/',views.CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',views.RegisterPage.as_view(),name='register'),
    path('taskorder/',views.TaskReorder.as_view(),name='TaskReorder'),
    


    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]