from django.contrib import admin
from .models import Ticket, TicketItem


class TicketItemInline(admin.TabularInline):
    model = TicketItem
    extra = 1
    fields = ['description', 'quantity', 'value']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'recipient_name', 'sender_name', 'shipping_date', 'carrier', 'created_at', 'pdf_generated', 'invoice_generated']
    list_filter = ['carrier', 'pdf_generated', 'invoice_generated', 'is_fragile', 'is_insured', 'created_at']
    search_fields = ['order_number', 'sender_name', 'recipient_name', 'tracking_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    inlines = [TicketItemInline]
    
    fieldsets = (
        ('Identification', {
            'fields': ('order_number', 'shipping_date', 'created_at')
        }),
        ('Expéditeur', {
            'fields': ('sender_name', 'sender_address', 'sender_city', 'sender_email', 'sender_phone')
        }),
        ('Destinataire', {
            'fields': ('recipient_name', 'recipient_address', 'recipient_city', 'recipient_email', 'recipient_phone', 'recipient_instructions')
        }),
        ('Colis', {
            'fields': ('weight', 'length', 'width', 'height', 'carrier', 'carrier_other', 'tracking_number')
        }),
        ('Options', {
            'fields': ('is_fragile', 'is_insured', 'insurance_amount', 'cash_on_delivery', 'signature_required', 'recipient_message')
        }),
        ('Métadonnées', {
            'fields': ('pdf_generated', 'invoice_generated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TicketItem)
class TicketItemAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'description', 'quantity', 'value', 'get_line_total']
    list_filter = ['ticket__created_at']
    search_fields = ['description', 'ticket__order_number']
    
    def get_line_total(self, obj):
        return f"{obj.get_line_total()} €"
    get_line_total.short_description = 'Total'
