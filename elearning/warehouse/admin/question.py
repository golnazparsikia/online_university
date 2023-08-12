from django.contrib import admin

from elearning.warehouse.models import Question

@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ('product',
                    'kind',
                    'modified',
                    'created'
                    )
    list_filter = (
        'kind',
        'modified',
        'created'
    )
    search_fields = (
        'kind',
    )
    readonly_fields = (
        'modified',
        'created'
    )
    save_on_top = True
    save_as = True 
