from django.contrib import admin

from . import models


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'answer', 'category',
                    'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('content',)

    # Limit the dropdown choices of category to user that created them
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = models.Category.objects.filter(
                                 user=request.user)
        return super(QuestionAdmin, self).formfield_for_foreignkey(
                                          db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    # Show only categories that the
    def get_queryset(self, request):
        return models.Category.objects.filter(user=request.user)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Question, QuestionAdmin)
