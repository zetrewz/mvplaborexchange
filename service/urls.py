from django.urls import path

from resume.favorites_logic import add_resume_in_favorites, check_in_favorites, remove_resume_in_favorites
from service.apply_logic import remove_application, check_application, apply
from service.views import feed, search
from vacancy.favorites_logic import check_vacancy_in_favorites, add_vacancy_in_favorites, remove_vacancy_in_favorites

app_name = 'service'

urlpatterns = [
    path('', feed, name='feed'),

    path('search/', search, name='search'),

    path('apply/<int:pk>/', apply, name='apply'),

    path('check_application/<int:pk>/',
         check_application,
         name='check_application'),

    path('remove_application/<int:pk>/',
         remove_application,
         name='remove_application'),

    path('add_resume_in_favorites/<int:pk>/',
         add_resume_in_favorites,
         name='add_resume_in_favorites'),

    path('check_in_favorites/<int:pk>/',
         check_in_favorites,
         name='check_in_favorites'),

    path('remove_resume_in_favorites/<int:pk>/',
         remove_resume_in_favorites,
         name='remove_resume_in_favorites'),

    path('add_vacancy_in_favorites/<int:pk>/',
         add_vacancy_in_favorites,
         name='add_vacancy_in_favorites'),

    path('check_vacancy_in_favorites/<int:pk>/',
         check_vacancy_in_favorites,
         name='check_vacancy_in_favorites'),

    path('remove_vacancy_in_favorites/<int:pk>/',
         remove_vacancy_in_favorites,
         name='remove_vacancy_in_favorites'),
]
