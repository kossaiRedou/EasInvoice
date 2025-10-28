from django.urls import path
from . import views

app_name = 'CORE'

urlpatterns = [
    path('', views.generate_invoice_form, name='invoice_form'),
    path('add-item-row/', views.add_item_row, name='add_item_row'),
]
