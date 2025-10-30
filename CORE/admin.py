from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'from_name', 'to_name', 'invoice_date', 'total', 'created_at', 'pdf_generated']
    list_filter = ['pdf_generated', 'is_vat_exempt', 'is_ei', 'created_at']
    search_fields = ['invoice_number', 'from_name', 'to_name', 'siret']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Lien avec étiquette', {
            'fields': ('ticket',),
            'classes': ('collapse',)
        }),
        ('Identification', {
            'fields': ('invoice_number', 'invoice_date', 'created_at')
        }),
        ('Émetteur', {
            'fields': ('from_name', 'from_address', 'from_city', 'from_email', 'siret', 'rcs', 'is_ei')
        }),
        ('Destinataire', {
            'fields': ('to_name', 'to_address', 'to_city', 'to_email')
        }),
        ('Dates', {
            'fields': ('service_date_start', 'service_date_end', 'due_date')
        }),
        ('Montants', {
            'fields': ('subtotal', 'vat_rate', 'vat_amount', 'total', 'is_vat_exempt')
        }),
        ('Conditions', {
            'fields': ('payment_terms', 'late_fee_rate', 'recovery_fee', 'autoliquidation')
        }),
        ('Métadonnées', {
            'fields': ('pdf_generated',),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'get_line_total']
    list_filter = ['invoice__created_at']
    search_fields = ['description', 'invoice__invoice_number']
    
    def get_line_total(self, obj):
        return f"{obj.get_line_total()} €"
    get_line_total.short_description = 'Total'
