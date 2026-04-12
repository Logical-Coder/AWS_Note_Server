from django.contrib import admin
from .models import QANote


@admin.register(QANote)
class QANoteAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'question_subtopic', 'question_format', 'read_count', 'short_question', 'created_at')
    list_filter = ('question_type', 'question_format', 'question_subtopic')
    search_fields = ('question', 'answer', 'question_subtopic')
    ordering = ('-read_count', '-created_at')
    fieldsets = (
        ('Question Info', {
            'fields': ('question', 'question_type', 'question_subtopic', 'question_format')
        }),
        ('Answer', {
            'fields': ('answer',)
        }),
        ('Attachment & Metadata', {
            'fields': ('attachment', 'read_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'read_count')

    def short_question(self, obj):
        return obj.question[:100]
    short_question.short_description = 'Question'
