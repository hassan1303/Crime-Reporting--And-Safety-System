from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import home, report, about, safety_tips, user_login, register, user_logout #profile

urlpatterns = [
    path('', home, name='home'),
    path('report/', report, name='report'),
    path('about/', about, name='about'),
    path('safety_tips/', safety_tips, name='safety_tips'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('admin/create_notification/', views.create_notification, name='create_notification'),
    path('notifications/<int:notification_id>/read/', views.read_notification, name='read_notification'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)