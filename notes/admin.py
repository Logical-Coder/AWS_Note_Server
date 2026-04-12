from django.contrib import admin
from .models import QANote


@admin.register(QANote)
class QANoteAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'short_question', 'created_at')
    list_filter = ('question_type',)
    search_fields = ('question', 'answer')
    ordering = ('-created_at',)

    def short_question(self, obj):
        return obj.question[:100]
    short_question.short_description = 'Question'
