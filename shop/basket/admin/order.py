from django.contrib import admin
from shop.basket.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_number",
        "status",
        "admin_note",
        "total_cost",
        "user",
        "created",
        "modified",
    )

    readonly_fields = (
        "transaction_number",
        "created",
        "modified",
        "total_cost",
    )
    
    list_filter = ('status',)

    search_fields = (
        "transaction_number",
    )
    
    fieldsets = (
        (("User Information"), {
            'fields': ('user',)
        }),

        (("Transaction Information"), {
            'fields': (
                'transaction_number',
                'status',
                'admin_note',
                'total_cost'
            )
        }),

        (("Security"), {
            'fields': (
                "created",
                "modified"
            ),
            'classes': ('collapse',)
        })
    )
