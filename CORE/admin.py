from django.contrib import admin
from .models import UserProfile, Client, Invoice, InvoiceItem, ContactMessage


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price', 'line_total']
    readonly_fields = ['line_total']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'city', 'siret', 'is_ei', 'created_at']
    search_fields = ['user__username', 'company_name', 'siret']
    list_filter = ['is_ei', 'created_at']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'city', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'user__username']
    list_filter = ['created_at', 'user']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'user', 'to_name', 'invoice_date', 'due_date', 'total', 'status', 'created_at']
    search_fields = ['invoice_number', 'to_name', 'from_name', 'user__username']
    list_filter = ['status', 'invoice_date', 'created_at', 'is_vat_exempt']
    inlines = [InvoiceItemInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'client', 'status')
        }),
        ('Émetteur', {
            'fields': ('from_name', 'from_address', 'from_city', 'from_email', 'siret', 'rcs', 'is_ei')
        }),
        ('Destinataire', {
            'fields': ('to_name', 'to_address', 'to_city', 'to_email')
        }),
        ('Informations facture', {
            'fields': ('invoice_number', 'invoice_date', 'service_date_start', 'service_date_end', 'due_date')
        }),
        ('Montants', {
            'fields': ('subtotal', 'vat_rate', 'vat_amount', 'total', 'is_vat_exempt')
        }),
        ('Conditions de paiement', {
            'fields': ('payment_terms', 'late_fee_rate', 'recovery_fee', 'autoliquidation')
        }),
        ('Notes et suivi', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'line_total', 'order']
    search_fields = ['description', 'invoice__invoice_number']
    list_filter = ['invoice__user']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'is_read', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'message']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at']
