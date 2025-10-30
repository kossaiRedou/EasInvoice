import json
import os
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.forms import formset_factory

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint non disponible: {e}")

from .forms import InvoiceForm, ItemForm


def _build_items_from_formset(items_formset):
    items = []
    for form in items_formset:
        if not form.is_valid():
            continue
        cleaned = form.cleaned_data
        if not cleaned:
            continue
        if cleaned.get('DELETE'):
            continue
        desc = cleaned.get('description')
        qty = cleaned.get('quantity')
        price = cleaned.get('unit_price')
        if desc and qty is not None and price is not None:
            line_total = Decimal(str(qty)) * Decimal(str(price))
            items.append({
                'description': desc,
                'quantity': float(qty),
                'unit_price': float(price),
                'line_total': float(line_total),
            })
    return items


def generate_invoice_form(request):
    """
    Affiche le formulaire de création de facture et génère le PDF si soumis.
    """
    ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        items_formset = ItemFormSet(request.POST, prefix='items')
        
        if form.is_valid() and items_formset.is_valid():
            data = form.cleaned_data

            items = _build_items_from_formset(items_formset)
            # Fallback: si aucun item, utiliser les champs simples si fournis
            if not items and data.get('description'):
                qty = Decimal(str(data.get('quantity') or 1))
                price = Decimal(str(data.get('unit_price') or 0))
                items = [{
                    'description': data['description'],
                    'quantity': float(qty),
                    'unit_price': float(price),
                    'line_total': float(qty * price),
                }]

            # Totaux
            subtotal = Decimal('0')
            for it in items:
                subtotal += Decimal(str(it['line_total']))

            # Gestion TVA
            is_vat_exempt = bool(data.get('is_vat_exempt'))
            vat_rate_input = data.get('vat_rate') if data.get('vat_rate') is not None else Decimal('0')
            vat_rate = Decimal('0') if is_vat_exempt else Decimal(str(vat_rate_input))
            vat_amount = subtotal * (vat_rate / 100)
            total = subtotal + vat_amount

            vat_note = "TVA non applicable, art. 293 B du CGI" if is_vat_exempt else None

            # Mentions paiement
            late_fee_rate = data.get('late_fee_rate')
            recovery_fee = bool(data.get('recovery_fee'))
            payment_terms = data.get('payment_terms') or ''
            penalties_note = f"Pénalités de retard: {late_fee_rate}%/an à compter du lendemain de la date d'échéance." if late_fee_rate else None
            recovery_note = "Indemnité forfaitaire de recouvrement: 40 € due en cas de retard de paiement." if recovery_fee else None
            autoliquidation = bool(data.get('autoliquidation'))

            context = {
                **data,
                'items': items,
                'is_vat_exempt': is_vat_exempt,
                'vat_rate': float(vat_rate),
                'subtotal': float(subtotal),
                'vat_amount': float(vat_amount),
                'total': float(total),
                'vat_note': vat_note,
                'payment_terms': payment_terms,
                'penalties_note': penalties_note,
                'recovery_note': recovery_note,
                'autoliquidation': autoliquidation,
            }

            html_string = render_to_string('CORE/invoice.html', context)

            if not WEASYPRINT_AVAILABLE:
                return HttpResponse(
                    "WeasyPrint n'est pas installé. Installez-le avec: pip install WeasyPrint",
                    status=500
                )

            try:
                # Charger le HTML sans base_url pour éviter requêtes réseau
                html = HTML(string=html_string, base_url=None)
                
                # Charger le CSS local de façon optimisée
                css_file = Path(__file__).resolve().parent.parent / 'static' / 'CORE' / 'css' / 'invoice.css'
                if css_file.exists():
                    pdf = html.write_pdf(stylesheets=[CSS(css_file)])
                else:
                    pdf = html.write_pdf()

                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"facture_{data['invoice_number']}_{datetime.now().strftime('%Y%m%d')}.pdf"
                response['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
                return response

            except Exception as e:
                import traceback
                return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}<br><pre>{traceback.format_exc()}</pre>", status=500)
    else:
        form = InvoiceForm(initial={
            'invoice_date': datetime.now().date(),
            'due_date': datetime.now().date(),
            'vat_rate': 20.00,
            'recovery_fee': True,
        })
        items_formset = ItemFormSet(prefix='items')
    
    return render(request, 'CORE/form.html', {
        'form': form,
        'items_formset': items_formset,
        'weasyprint_available': WEASYPRINT_AVAILABLE
    })


def add_item_row(request):
    """HTMX endpoint: retourne une ligne d'item vide et met à jour TOTAL_FORMS."""
    total_forms = request.POST.get('items-TOTAL_FORMS') or request.GET.get('items-TOTAL_FORMS')
    try:
        current_idx = int(total_forms)
    except (TypeError, ValueError):
        current_idx = 0
    new_index = current_idx
    ItemFormSet = formset_factory(ItemForm, extra=0, can_delete=True)
    dummy_formset = ItemFormSet(prefix='items')
    form = dummy_formset.empty_form
    # Adapter le prefix de __prefix__ à l'index courant
    form.prefix = f'items-{new_index}'
    row_html = render_to_string('CORE/_item_row.html', {'form': form, 'index': new_index})
    mgmt_html = f'\n<input type="hidden" name="items-TOTAL_FORMS" id="id_items-TOTAL_FORMS" value="{new_index + 1}" hx-swap-oob="true">\n'
    return HttpResponse(row_html + mgmt_html)


def privacy_policy(request):
    """Page de politique de confidentialité"""
    return render(request, 'CORE/privacy_policy.html')


def invoice_from_ticket(request):
    """
    Génère une facture pré-remplie avec les données d'une étiquette
    """
    ticket_id = request.session.get('last_ticket_id')
    
    if not ticket_id:
        # Pas d'étiquette en session, redirection vers formulaire vide
        return redirect('CORE:invoice_form')
    
    try:
        from TICKET.models import Ticket
        ticket = Ticket.objects.get(id=ticket_id)
    except:
        # Étiquette introuvable, redirection vers formulaire vide
        return redirect('CORE:invoice_form')
    
    ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        items_formset = ItemFormSet(request.POST, prefix='items')
        
        if form.is_valid() and items_formset.is_valid():
            data = form.cleaned_data
            items = _build_items_from_formset(items_formset)
            
            # Fallback: si aucun item, utiliser les champs simples si fournis
            if not items and data.get('description'):
                qty = Decimal(str(data.get('quantity') or 1))
                price = Decimal(str(data.get('unit_price') or 0))
                items = [{
                    'description': data['description'],
                    'quantity': float(qty),
                    'unit_price': float(price),
                    'line_total': float(qty * price),
                }]
            
            # Totaux
            subtotal = Decimal('0')
            for it in items:
                subtotal += Decimal(str(it['line_total']))
            
            # Gestion TVA
            is_vat_exempt = bool(data.get('is_vat_exempt'))
            vat_rate_input = data.get('vat_rate') if data.get('vat_rate') is not None else Decimal('0')
            vat_rate = Decimal('0') if is_vat_exempt else Decimal(str(vat_rate_input))
            vat_amount = subtotal * (vat_rate / 100)
            total = subtotal + vat_amount
            
            vat_note = "TVA non applicable, art. 293 B du CGI" if is_vat_exempt else None
            
            # Mentions paiement
            late_fee_rate = data.get('late_fee_rate')
            recovery_fee = bool(data.get('recovery_fee'))
            payment_terms = data.get('payment_terms') or ''
            penalties_note = f"Pénalités de retard: {late_fee_rate}%/an à compter du lendemain de la date d'échéance." if late_fee_rate else None
            recovery_note = "Indemnité forfaitaire de recouvrement: 40 € due en cas de retard de paiement." if recovery_fee else None
            autoliquidation = bool(data.get('autoliquidation'))
            
            context = {
                **data,
                'items': items,
                'is_vat_exempt': is_vat_exempt,
                'vat_rate': float(vat_rate),
                'subtotal': float(subtotal),
                'vat_amount': float(vat_amount),
                'total': float(total),
                'vat_note': vat_note,
                'payment_terms': payment_terms,
                'penalties_note': penalties_note,
                'recovery_note': recovery_note,
                'autoliquidation': autoliquidation,
            }
            
            html_string = render_to_string('CORE/invoice.html', context)
            
            if not WEASYPRINT_AVAILABLE:
                return HttpResponse(
                    "WeasyPrint n'est pas installé. Installez-le avec: pip install WeasyPrint",
                    status=500
                )
            
            try:
                # Charger le HTML sans base_url pour éviter requêtes réseau
                html = HTML(string=html_string, base_url=None)
                
                # Charger le CSS local de façon optimisée
                css_file = Path(__file__).resolve().parent.parent / 'static' / 'CORE' / 'css' / 'invoice.css'
                if css_file.exists():
                    pdf = html.write_pdf(stylesheets=[CSS(css_file)])
                else:
                    pdf = html.write_pdf()
                
                # Marquer l'étiquette comme facturée
                ticket.invoice_generated = True
                ticket.save()
                
                # Nettoyer la session
                if 'last_ticket_id' in request.session:
                    del request.session['last_ticket_id']
                
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"facture_{data['invoice_number']}_{datetime.now().strftime('%Y%m%d')}.pdf"
                response['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
                return response
                
            except Exception as e:
                import traceback
                return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}<br><pre>{traceback.format_exc()}</pre>", status=500)
    
    else:
        # Pré-remplir le formulaire avec les données de l'étiquette
        from datetime import date
        initial_data = {
            'from_name': ticket.sender_name,
            'from_address': ticket.sender_address,
            'from_city': ticket.sender_city,
            'from_email': ticket.sender_email or '',
            'to_name': ticket.recipient_name,
            'to_address': ticket.recipient_address,
            'to_city': ticket.recipient_city,
            'to_email': ticket.recipient_email or '',
            'invoice_number': ticket.order_number,
            'invoice_date': date.today(),
            'due_date': date.today(),
            'service_date_start': ticket.shipping_date,
            'vat_rate': 20.00,
            'recovery_fee': True,
        }
        
        form = InvoiceForm(initial=initial_data)
        
        # Items depuis l'étiquette
        initial_items = [
            {
                'description': item.description,
                'quantity': item.quantity,
                'unit_price': item.value,
            }
            for item in ticket.items.all()
        ]
        
        if initial_items:
            items_formset = ItemFormSet(initial=initial_items, prefix='items')
        else:
            items_formset = ItemFormSet(prefix='items')
    
    return render(request, 'CORE/form.html', {
        'form': form,
        'items_formset': items_formset,
        'weasyprint_available': WEASYPRINT_AVAILABLE,
        'prefilled_from_ticket': True,
        'ticket': ticket,
    })
