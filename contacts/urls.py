from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactsDetailView.as_view(), name='contacts'),
    path('ukraine/', views.ContactsDetailView.as_view(), {'country': 'ukraine'}, name='ukraine'),
    path('bulgaria/', views.ContactsDetailView.as_view(), {'country': 'bulgaria'}, name='bulgaria'),
    path('china/', views.ContactsDetailView.as_view(), {'country': 'china'}, name='china'),

    path('form/', views.CompanyFormView.as_view(), name="contact_form")
]