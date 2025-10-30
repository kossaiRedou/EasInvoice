from django.urls import path
from . import views

app_name = 'TICKET'

urlpatterns = [
    path('', views.generate_ticket, name='ticket_form'),
    path('add-package-item/', views.add_package_item, name='add_package_item'),
]

