from django.contrib import admin
from ..models import OneTimePassword

@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'masked_token',
        'expiry_time',
        'reason',
        'state',
        'type'
    )
    list_filter = (
        'reason',
        'state',
        'type'
    )
    search_fields = ('user__username',)
    list_per_page = 25

    def masked_token(self, obj):
        return '*' * (len(obj.token) - 4) + obj.token[-4:]
    
    masked_token.short_description = 'Token'

