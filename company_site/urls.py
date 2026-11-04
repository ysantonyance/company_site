from django.urls import path
from . import views

urlpatterns = [
    path('',               views.home,        name='home'),
    path('news/',          views.news,        name='news'),
    path('management/',    views.management,  name='management'),
    path('about/',         views.about,       name='about'),
    path('contacts/',      views.contacts,    name='contacts'),
    path('contact/',       views.contacts,    name='contact-alt'),

    # сatch-all для кожного розділу (найважливіше — порядок!)
    path('news/<path:_>/',      views.news,       name='news-catchall'),
    path('management/<path:_>/',views.management, name='mgmt-catchall'),
    path('about/<path:_>/',     views.about,      name='about-catchall'),
    path('contacts/<path:_>/',  views.contacts,   name='contacts-catchall'),
    path('contact/<path:_>/',   views.contacts,   name='contact-alt-catchall'),
]