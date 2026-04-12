from django.contrib import admin
from .models import QANote, Answer


@admin.register(QANote)
class QANoteAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'question_subtopic', 'question_format', 'read_count', 'short_question', 'answer_count', 'created_at')
    list_filter = ('question_type', 'question_format', 'question_subtopic')
    search_fields = ('question', 'question_subtopic')
    ordering = ('-read_count', '-created_at')
    fieldsets = (
        ('Question Info', {
            'fields': ('question', 'question_type', 'question_subtopic', 'question_format')
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

    def answer_count(self, obj):
        return obj.answers.count()
    answer_count.short_description = 'Answers'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'short_answer', 'read_count', 'created_at')
    list_filter = ('created_at', 'read_count')
    search_fields = ('answer_text', 'question__question')
    ordering = ('-read_count', '-created_at')
    readonly_fields = ('created_at',)

    def short_answer(self, obj):
        return obj.answer_text[:100]
    short_answer.short_description = 'Answer'
