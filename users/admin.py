from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'login_user', 'email', 'is_staff', 'is_active',
    )
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': (
            'login_user', 'email', 'password'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'login_user', 'email', 'password1', 'password2',
                'is_staff', 'is_active'
            )}
        ),
    )

    search_fields = ('email',)
    ordering = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)
