from django.urls import path
from . import views

app_name = 'CORE'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    path('contact/', views.contact_submit, name='contact_submit'),
    
    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Factures
    path('invoice/new/', views.generate_invoice_form, name='generate_invoice'),
    path('invoice/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.invoice_download_pdf, name='invoice_download_pdf'),
    path('invoice/<int:invoice_id>/update-status/', views.invoice_update_status, name='invoice_update_status'),
    path('invoice/<int:invoice_id>/delete/', views.invoice_delete, name='invoice_delete'),
    
    # HTMX
    path('add-item-row/', views.add_item_row, name='add_item_row'),
    
    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    
    # Profil utilisateur
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Autres
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
