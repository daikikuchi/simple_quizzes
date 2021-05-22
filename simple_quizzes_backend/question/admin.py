from django.contrib import admin
from . import models


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'answer', 'category',
                    'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('content',)


admin.site.register(models.Category)
admin.site.register(models.Question, QuestionAdmin)
