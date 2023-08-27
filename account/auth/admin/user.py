from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

# Register the User model with the custom admin class
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Fields displayed in the list view of users
    list_display = (
        'phone_number',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    # Filters displayed on the right side
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
    )

    # Fields that can be searched for users
    search_fields = (
        'phone_number',
        'email',
        'first_name',
        'last_name',
    )

    # Help text for search
    search_help_text = 'You can look for users by first name, last name, phone number, or email.'

    # Save buttons on top
    save_on_top = True

    # Fields that are read-only
    readonly_fields = (
        'username',
        'phone_number',
    )

    # Ordering of users in the list view
    ordering = (
        '-date_joined',
    )

    # Configuration of different sections in the user edit page
    fieldsets = (
        (None, {
            'fields': (
                'phone_number',
                'password',
            )
        }),
        ('Personal Info', {
            'fields': (
                'email',
                'first_name',
                'last_name',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Security', {
            'fields': (
                'last_login',
                'date_joined',
            )
        })
    )
