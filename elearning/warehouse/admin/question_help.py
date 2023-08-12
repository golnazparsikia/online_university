from django.contrib import admin

from elearning.warehouse.models import QuestionHelp

@admin.register(QuestionHelp)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('question',
                    'modified',
                    'created'
                    )
    list_filter = (
        'modified',
        'created'
    )
    search_fields = (
        'question',
    )
    readonly_fields = (
        'modified',
        'created',
    )
    save_on_top = True
    save_as = True 
