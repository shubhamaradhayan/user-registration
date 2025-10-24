
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')
    
    # Fields for filtering in the right sidebar
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    
    # Fields grouped in the edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_image')}),
        ('Address', {'fields': ('address_line', 'city', 'state', 'pincode')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('user_type',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields shown when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
