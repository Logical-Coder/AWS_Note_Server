from django.contrib import admin
from .models import QANote, Answer


@admin.register(QANote)
class QANoteAdmin(admin.ModelAdmin):
    list_display  = ('question_type', 'question_format', 'short_question', 'question_subtopic', 'read_count', 'created_at')
    list_filter   = ('question_type', 'question_format')
    search_fields = ('question', 'answer', 'question_subtopic')
    ordering      = ('read_count', '-created_at')

    def short_question(self, obj):
        return obj.question[:100]
    short_question.short_description = 'Question'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display  = ('question', 'read_count', 'created_at')
    search_fields = ('answer_text',)
    ordering      = ('read_count', '-created_at')
