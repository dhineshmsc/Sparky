
from django.contrib import admin
from django.urls import path
from assign_task import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'), 
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_user, name='logout'), 
    path('task_assing/', views.task_assign, name='task_assign'), 
    path('DEP_1/', views.DEP_1, name='DEP_1'), 
    path('update/<int:num>', views.update, name='update'), 
    path('sum/<int:num>', views.sum, name='sum'),
    path('welcome/<int:num>/<str:name>/', views.welcome, name='welcome'),
]
