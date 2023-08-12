from django.contrib import admin

from elearning.warehouse.models import Answer

@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ('is_correct',
                    'modified',
                    'created'
                    )
    list_filter = (
        'is_correct',
        'modified',
        'created'
    )
    readonly_fields = (
        'modified',
        'created',
    )
    save_on_top = True
    save_as = True 
