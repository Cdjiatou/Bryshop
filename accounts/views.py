from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from .forms import UserForm, ClientForm,UserUpdateForm, ClientUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.decorators import login_required 
from BRYSHOP.models import Order 

from .models import Notification


from django.contrib import messages

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            login(request, user)
            messages.success(request, f"Bienvenue sur BryShop, {user.username} ! 🎉")
            return redirect('login')  # ou ta page d’accueil
    else:
        user_form = UserForm()
        client_form = ClientForm()

    return render(request, 'html/register.html', {
        'user_form': user_form,
        'client_form': client_form
    })




class CustomLoginView(LoginView):
    template_name = 'html/login.html'

    def form_valid(self, form):
        # Ajouter le message ici
        user = form.get_user()
        messages.success(self.request, f"Bienvenue {user.username} ! Heureux de vous revoir 😄")
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'boutiquier':
            return reverse_lazy('dashboard_boutiquier')
        return self.get_redirect_url() or reverse_lazy('Accueil')



    
def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"👋 {username}, vous avez été déconnecté avec succès.")
    return redirect('Accueil')  # Redirige vers l'accueil




@login_required
def profile_view(request):
    user = request.user
    
    # Historique des commandes de l'utilisateur
    user_orders = Order.objects.filter(user=user).order_by('-date_ordered')

    # Initialisation des formulaires
    try:
        client_instance = user.client 
    except:
        # Gérer le cas où l'utilisateur n'a pas de modèle Client associé (improbable si l'inscription fonctionne)
        client_instance = None
    
    # Le UserForm est un peu délicat car nous ne voulons pas le password ici.
    # Nous allons utiliser les modèles directement pour l'affichage et les formulaires de gestion
    # pour les modifications (sauf le mot de passe).

    # Formulaire de changement de mot de passe
    password_form = PasswordChangeForm(user=user)
    
    context = {
        'user': user,
        'client': client_instance,
        'user_orders': user_orders,
        'password_form': password_form,
        'tab': 'dashboard' # Onglet actif par défaut
    }
    
    return render(request, 'html/profile.html', context)





@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Important : Garde l'utilisateur connecté après le changement de mot de passe
            update_session_auth_hash(request, user)  
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès !')
            return redirect('profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(user=request.user)

    # Réutilise le template de profil pour afficher le formulaire de mot de passe
    # et s'assurer que le bon onglet est actif.
    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    try:
        client_instance = request.user.client 
    except:
        client_instance = None

    context = {
        'user': request.user,
        'client': client_instance,
        'user_orders': user_orders,
        'password_form': form,
        'tab': 'security' # Indique que l'onglet Sécurité doit être actif
    }
    return render(request, 'html/profile.html', context)



@login_required
def notifications_view(request):
    # Récupère toutes les notifications de l'utilisateur
    notifications = Notification.objects.filter(user=request.user)
    
    # Compte les notifications non lues
    unread_count = notifications.filter(is_read=False).count()
    
    # Nous allons utiliser le template de profil, mais avec un onglet spécifique
    user = request.user
    user_orders = Order.objects.filter(user=user).order_by('-date_ordered')
    password_form = PasswordChangeForm(user=user)

    context = {
        'user': user,
        'user_orders': user_orders,
        'password_form': password_form,
        'notifications': notifications, # <--- AJOUTEZ CETTE LIGNE
        'unread_count': unread_count,   # <--- AJOUTEZ CETTE LIGNE
        'tab': 'notifications' # Onglet actif
    }
    return render(request, 'html/profile.html', context)


@login_required
def mark_notification_read(request, notification_id):
    # Sécurité : s'assure que la notification appartient bien à l'utilisateur
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        user=request.user
    )
    
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
        
        # Redirige vers l'URL de la notification si elle en a une, sinon vers la liste
        if notification.url:
            return redirect(notification.url)
        else:
            return redirect('notifications_list')

    return redirect('notifications_list') 




@login_required
def profile_update(request):
    user_form = UserUpdateForm(instance=request.user)
    client_form = ClientUpdateForm(instance=request.user.client)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        client_form = ClientUpdateForm(request.POST, instance=request.user.client)

        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            messages.success(request, 'Votre profil a ete mis a jour avec succes.')
            return redirect('profile') 
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

    context = {
        'user_form': user_form,
        'client_form': client_form,
        'tab': 'dashboard' # S'assurer que le tab 'dashboard' reste actif
    }
    # Rendu du template dédié à la mise à jour
    return render(request, 'html/profile_update.html', context)