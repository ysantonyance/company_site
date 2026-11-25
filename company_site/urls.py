from email.policy import default
from xml.etree.ElementInclude import include

from django.urls import path, include
from django.views import defaults as default_views
from django.contrib import admin
from company.views import index
from . import views

urlpatterns = [
    path('',               views.home,        name='home'),
    path('news/',          views.news,        name='news'),
    path('management/',    views.management,  name='management'),
    path('about/',         views.about,       name='about'),

    path('contacts/', include('contacts.urls')),

    path('contact/', include('contacts.urls'), name='contact-alt'),

    path('404/', default_views.page_not_found),
    path('admin/', admin.site.urls),
    path('company/', index, name='company_panel'),

    # сatch-all для кожного розділу (найважливіше — порядок!)
    path('news/<path:_>/',      views.news,       name='news-catchall'),
    path('management/<path:_>/',views.management, name='mgmt-catchall'),
    path('about/<path:_>/',     views.about,      name='about-catchall'),
    path('contacts/<path:_>/',  views.contacts,   name='contacts-catchall'),
    path('contact/<path:_>/',   views.contacts,   name='contact-alt-catchall'),
]