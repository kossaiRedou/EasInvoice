from django.urls import path
from . import views

app_name = 'CORE'

urlpatterns = [
    path('', views.generate_invoice_form, name='invoice_form'),
    path('add-item-row/', views.add_item_row, name='add_item_row'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('facture-depuis-etiquette/', views.invoice_from_ticket, name='invoice_from_ticket'),
]
