from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserForm, ClientForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy



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
        return self.get_redirect_url() or reverse_lazy('Accueil')



    
def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"👋 {username}, vous avez été déconnecté avec succès.")
    return redirect('Accueil')  # Redirige vers l'accueil