from django.urls import path, include
from . import views
from .views import edit_stats_agility, edit_stats_stamina, edit_stats_strength, profile, get_rank, update_profile_picture, submit_form, submit_media_form, leaderboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('accounts/', include('allauth.urls')),
    path('admin/', submit_form, name='submit_form'),
    path('profile/', views.profile, name="profile"),
    path('profile/update/', update_profile_picture, name='update_profile_picture'),
    path('submit-media/', submit_media_form, name='submit_media_form'),
    path('edit-stats/strength/', views.edit_stats_strength, name='edit_stats_strength'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('edit-stats/agility/', views.edit_stats_agility, name='edit_stats_agility'),
    path('edit-stats/stamina/', views.edit_stats_stamina, name='edit_stats_stamina'),



    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

