from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # protecção para os staffs não verem outros staffs
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True, is_staff=True)

        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser and obj is not None:
            form.base_fields['username'].disable = True
            form.base_fields['is_superuser'].disable = True
            form.base_fields['user_permissions'].disable = True
            form.base_fields['groups'].disable = True
            form.base_fields['is_active'].disabled = True
            form.base_fields['is_staff'].disable = True

        return form
    
    list_display = ('username', 'email')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissões', {'fields': ( 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


admin.site.register(Usuario, CustomUserAdmin)
