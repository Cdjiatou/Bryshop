from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		('Informations supplémentaires', {'fields': ('telephone', 'ville', 'pays', 'sexe', 'role')}),
	)
	list_display = UserAdmin.list_display + ('role',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('user', 'sexe', 'telephone', 'ville', 'pays')
