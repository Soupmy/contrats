from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Unite

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'unite')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('unite',)}),
    )
@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display = ('nom_site', 'created_by')
    exclude = ('created_by',)  # Ne pas afficher dans le formulaire

    def save_model(self, request, obj, form, change):
        # Assigner automatiquement l'utilisateur connecté
        if not change:  # Seulement à la création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('unite',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)