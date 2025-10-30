from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from datetime import datetime, date
from pathlib import Path

from .models import Ticket, TicketItem
from .forms import TicketForm, PackageItemFormSet

# Import WeasyPrint avec gestion d'erreur
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False


def generate_ticket(request):
    """Vue principale pour générer une étiquette"""
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        item_formset = PackageItemFormSet(request.POST, prefix='items')
        
        if form.is_valid() and item_formset.is_valid():
            # Sauvegarder l'étiquette
            ticket = form.save()
            
            # Sauvegarder les articles
            for item_form in item_formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = TicketItem(
                        ticket=ticket,
                        description=item_form.cleaned_data['description'],
                        quantity=item_form.cleaned_data['quantity'],
                        value=item_form.cleaned_data['value']
                    )
                    item.save()
            
            # Préparer les données pour le template
            data = {
                'ticket': ticket,
                'items': ticket.items.all(),
                'total_value': ticket.get_total_value(),
            }
            
            # Générer le PDF
            if not WEASYPRINT_AVAILABLE:
                return HttpResponse(
                    "WeasyPrint n'est pas installé. Installez-le avec: pip install WeasyPrint",
                    status=500
                )
            
            try:
                template = loader.get_template('TICKET/ticket_label.html')
                html_string = template.render(data, request)
                
                # Charger le HTML sans base_url pour éviter requêtes réseau
                html = HTML(string=html_string, base_url=None)
                
                # Charger le CSS local de façon optimisée
                css_file = Path(__file__).resolve().parent.parent / 'static' / 'TICKET' / 'css' / 'label.css'
                if css_file.exists():
                    pdf = html.write_pdf(stylesheets=[CSS(css_file)])
                else:
                    pdf = html.write_pdf()
                
                # Marquer le PDF comme généré
                ticket.pdf_generated = True
                ticket.save()
                
                # Sauvegarder l'ID en session pour la facture
                request.session['last_ticket_id'] = ticket.id
                request.session['ticket_generated'] = True
                
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"etiquette_{ticket.order_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
                
            except Exception as e:
                import traceback
                return HttpResponse(
                    f"Erreur lors de la génération du PDF: {str(e)}<br><pre>{traceback.format_exc()}</pre>",
                    status=500
                )
    
    else:
        form = TicketForm(initial={'shipping_date': date.today()})
        item_formset = PackageItemFormSet(prefix='items')
    
    # Vérifier si une étiquette vient d'être générée
    ticket_generated = request.session.pop('ticket_generated', False)
    last_ticket_id = request.session.get('last_ticket_id')
    last_ticket = None
    
    if last_ticket_id:
        try:
            last_ticket = Ticket.objects.get(id=last_ticket_id)
        except Ticket.DoesNotExist:
            pass
    
    context = {
        'form': form,
        'item_formset': item_formset,
        'ticket_generated': ticket_generated,
        'last_ticket': last_ticket,
    }
    
    return render(request, 'TICKET/ticket_form.html', context)


def add_package_item(request):
    """Vue HTMX pour ajouter une ligne d'article"""
    # Récupérer l'index actuel depuis le formulaire
    total_forms = request.GET.get('items-TOTAL_FORMS', '0')
    
    try:
        index = int(total_forms)
    except ValueError:
        index = 0
    
    # Créer un formset vide pour obtenir un nouveau formulaire
    item_formset = PackageItemFormSet(prefix='items')
    empty_form = item_formset.empty_form
    
    # Remplacer __prefix__ par l'index réel
    form_html = str(empty_form).replace('__prefix__', str(index))
    
    # Rendre le template partiel
    context = {
        'form': empty_form,
        'index': index,
        'form_html': form_html,
    }
    
    return render(request, 'TICKET/_package_item.html', context)
