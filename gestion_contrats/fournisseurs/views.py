from django.shortcuts import render, redirect, get_object_or_404
from .models import JuridiqueFournisseur
from .forms import FournisseurForm, BlacklistFournisseurForm
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from openpyxl import Workbook

# Create your views here.

# Exportation en fichier excell
@login_required
def export_blacklist_excel(request):
# Création du fichier
    wb = Workbook()
    ws = wb.active
    ws.title = "Fournisseur"
    # En-tetes
    ws.append(["ID", "NOM_DU_CONTRACTANT", "NUM_FIXE", "EMAIL", "NIF", "DATE_EXCLUSION", "DUREE_EXCLUSION", "DATE_LEVEE_SANCTION", "ETAT", "TYPE", "STRUCTURE_AYANT_EXCLU", "MOTIFS", "REMARQUES", "ACTIVITE", "ADRESSE", "VILLE", "CODE_POSTAL", "WILAYA", "TELEPHONE"])

    for f in JuridiqueFournisseur.objects.all():
        ws.append([
            f.id,
            f.nom_du_contractant,
            f.num_fixe,
            f.email,
            f.nif,
            f.date_exclusion,
            f.duree_exclusion,
            f.date_levee_sanction,
            f.etat,
            f.type,
            f.structure_ayant_exclu,
            f.motifs,
            f.remarques,
            f.activite,
            f.adresse,
            f.ville,
            f.code_postal,
            f.wilaya,
            f.telephone,
        ])

    # Préparer la réponse HTTP pour le téléchargement
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fournisseurs-blacklists.xlsx'
    wb.save(response)
    return response


# Exportation en fichier excell
@login_required
def export_fournisseurs_excel(request):
    # Création du fichier
    wb = Workbook()
    ws = wb.active
    ws.title = "Fournisseur"
    # En-tetes
    ws.append(["ID", "NOM_DU_CONTRACTANT", "NUM_FIXE", "FAX", "EMAIL", "NIF", "DATE_EXCLUSION", "DUREE_EXCLUSION", "DATE_LEVEE_SANCTION", "ETAT", "TYPE", "STRUCTURE_AYANT_EXCLU", "MOTIFS", "REMARQUES", "ACTIVITE", "ADRESSE", "VILLE", "CODE_POSTAL", "WILAYA", "N_IDENTIFICATION_FISCALE", "N_IDENTIFICATION_STATISTIQUE", "N_REGISTRE_COMMERCE", "ARTICLE_IMPOSITION", "SYSTEME_NUMEROTATION_UNIVERSEL", "CARTE_ARTISANT",	"NUM_AGREMENT", "CRIT_RECH_1", "RUE", "NUMERO", "TELEPHONE", "TELEPHONE_2", "FORME_JURDIQUE",	"BRANCHE",	"TYPE_PARTENAIRE",	"CLE_PAYS_BANQUE",	"CLE_BANCAIRE",	"COMPTE_BANCAIRE",	"CLE_CONTROLE_BANCAIRE",])

    for f in JuridiqueFournisseur.objects.all():
        ws.append([
            f.id,
            f.nom_du_contractant,
            f.num_fixe,
            f.fax,
            f.email,
            f.nif,
            f.date_exclusion,
            f.duree_exclusion,
            f.date_levee_sanction,
            f.etat,
            f.type,
            f.structure_ayant_exclu,
            f.motifs,
            f.remarques,
            f.activite,
            f.adresse,
            f.ville,
            f.code_postal,
            f.wilaya,
            f.n_identification_fiscale,
            f.n_identification_statistique,
            f.n_registre_commerce,
            f.article_imposition,
            f.systeme_numerotation_universel,
            f.carte_artisant,
            f.num_agrement,
            f.crit_rech_1,
            f.rue,
            f.numero,
            f.telephone,
            f.telephone_2,
            f.forme_jurdique,
            f.branche,
            f.type_partenaire,
            f.cle_pays_banque,
            f.cle_bancaire,
            f.compte_bancaire,
            f.cle_controle_bancaire,
        ])

    # Préparer la réponse HTTP pour le téléchargement
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fournisseurs.xlsx'
    wb.save(response)
    return response

# Affichage fournisseurs et ajout 
@login_required
def fournisseurs_view(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseurs')  # Redirige vers la même page après l'ajout
    else:
        form = FournisseurForm()
         
    fournisseurs = JuridiqueFournisseur.objects.all()
    return render(request, 'fournisseurs/fournisseurs.html', {'fournisseurs': fournisseurs, 'form': form})

# Affichage détails fournisseur en fonction de l'id
@login_required
def fournisseurs_details(request, fournisseur_id):
    fournisseurs = get_object_or_404(JuridiqueFournisseur, id=fournisseur_id)
    field_values = {field.name: getattr(fournisseurs, field.name) for field in fournisseurs._meta.fields}
    return JsonResponse(field_values)


@login_required
def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)

    if request.method == 'POST'and request.POST.get('_method') == 'DELETE':
        fournisseur.delete()
        return JsonResponse({'success': True})
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'fournisseur': str(fournisseur)})

    # Sinon, requête non valide
    return JsonResponse({'success': False, 'error': 'Requête invalide'})
    




@login_required
def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/modifier_fournisseur_form.html', {'form': form})


@login_required
def blacklist_view(request):
    filtre = request.GET.get('filtre', 'all')
    
    if filtre == 'temporaire':
        fournisseurs = JuridiqueFournisseur.objects.filter(
            etat='BLACKLISTE', 
            date_levee_sanction__isnull=False
        )
    elif filtre == 'a_vie':
        fournisseurs = JuridiqueFournisseur.objects.filter(
            etat='BLACKLISTE', 
            date_levee_sanction__isnull=True
        )
    else:  # 'all'
        fournisseurs = JuridiqueFournisseur.objects.filter(etat='BLACKLISTE')
    
    # Liste des fournisseurs qui ne sont pas encore blacklistés
    fournisseurs_disponibles = JuridiqueFournisseur.objects.filter(etat='HABILITE')
    
    context = {
        'filtre': filtre,
        'fournisseurs': fournisseurs,
        'fournisseurs_disponibles': fournisseurs_disponibles,
    }
    
    return render(request, 'fournisseurs/blacklist.html', context)

@login_required
def blacklister_fournisseur(request):
    if request.method == 'POST':
        # Debug avant validation
        print("Données POST reçues:", request.POST)
        
        # Récupérer le fournisseur directement depuis l'ID
        fournisseur_id = request.POST.get('fournisseur_id')
        if not fournisseur_id:
            messages.error(request, "Aucun fournisseur sélectionné")
            return redirect('blacklist')
            
        try:
            fournisseur = JuridiqueFournisseur.objects.get(id=fournisseur_id)
        except JuridiqueFournisseur.DoesNotExist:
            messages.error(request, "Fournisseur introuvable")
            return redirect('blacklist')
        
        # Appliquer les modifications
        fournisseur.etat = 'BLACKLISTE'
        fournisseur.structure_ayant_exclu = request.POST.get('structure_ayant_exclu', '')
        fournisseur.motifs = request.POST.get('motifs', '')
        fournisseur.remarques = request.POST.get('remarques', '')
        
        blacklist_type = request.POST.get('blacklist_type', 'temporaire')
        if blacklist_type == 'temporaire':
            fournisseur.date_exclusion = request.POST.get('date_exclusion')
            fournisseur.duree_exclusion = request.POST.get('duree_exclusion', '')
            fournisseur.date_levee_sanction = request.POST.get('date_levee_sanction')
        else:
            fournisseur.date_exclusion = datetime.date.today()
            fournisseur.duree_exclusion = 'Permanente'
            fournisseur.date_levee_sanction = None
        
        # Debug avant sauvegarde
        print("Fournisseur à sauvegarder:", {
            'nom': fournisseur.nom_du_contractant,
            'etat': fournisseur.etat,
            'date_exclusion': fournisseur.date_exclusion,
            'motifs': fournisseur.motifs
        })
        
        fournisseur.save()
        messages.success(request, f"Le fournisseur {fournisseur.nom_du_contractant} a été blacklisté avec succès.")
        return redirect('blacklist')
    
    messages.error(request, "Méthode non autorisée")
    return redirect('blacklist')