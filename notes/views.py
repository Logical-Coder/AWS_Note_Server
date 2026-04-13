import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import QANote, Answer


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _resolve_type(post_data):
    """
    If the user selected '__custom__' from the dropdown,
    use the text they typed in custom_type field instead.
    Normalises to lowercase-with-underscores.
    """
    question_type = post_data.get('question_type', 'other')
    custom_type   = post_data.get('custom_type', '').strip()

    if question_type == '__custom__' and custom_type:
        question_type = custom_type.lower().replace(' ', '_')[:50]
    elif not question_type or question_type == '__custom__':
        question_type = 'other'

    return question_type


def _build_type_choices():
    """
    Predefined choices + any custom types already in the DB,
    returned as a flat list of (value, display_label) tuples.
    """
    predefined      = list(QANote.QUESTION_TYPE_CHOICES)
    predefined_keys = {v for v, _ in predefined}

    db_types = (
        QANote.objects
        .exclude(question_type__in=predefined_keys)
        .values_list('question_type', flat=True)
        .distinct()
        .order_by('question_type')
    )

    custom = [
        (t, t.replace('_', ' ').title())
        for t in db_types if t
    ]

    return predefined + custom


# ──────────────────────────────────────────────────────────────────────────────
# Views
# ──────────────────────────────────────────────────────────────────────────────

def home(request):
    if request.method == 'POST':
        question          = request.POST.get('question', '').strip()
        answer            = request.POST.get('answer', '')
        question_type     = _resolve_type(request.POST)
        question_subtopic = request.POST.get('question_subtopic', '').strip()
        question_format   = request.POST.get('question_format', 'description')
        attachment        = request.FILES.get('attachment')

        if question:
            QANote.objects.create(
                question=question,
                answer=answer,
                question_type=question_type,
                question_subtopic=question_subtopic,
                question_format=question_format,
                attachment=attachment,
            )
        return redirect('home')

    filter_type     = request.GET.get('type', '')
    filter_subtopic = request.GET.get('subtopic', '')
    filter_format   = request.GET.get('format', '')
    search_query    = request.GET.get('q', '')

    notes = QANote.objects.all()

    if filter_type:
        notes = notes.filter(question_type=filter_type)
    if filter_subtopic:
        notes = notes.filter(question_subtopic=filter_subtopic)
    if filter_format:
        notes = notes.filter(question_format=filter_format)
    if search_query:
        notes = notes.filter(question__icontains=search_query) | \
                notes.filter(answer__icontains=search_query)

    return render(request, 'notes/home.html', {
        'notes':            notes,
        'type_choices':     _build_type_choices(),
        'format_choices':   QANote.QUESTION_FORMAT_CHOICES,
        'subtopics_json':   json.dumps(QANote.QUESTION_SUBTOPICS),
        'filter_type':      filter_type,
        'filter_subtopic':  filter_subtopic,
        'filter_format':    filter_format,
        'search_query':     search_query,
    })


def edit_note(request, note_id):
    note = get_object_or_404(QANote, id=note_id)

    if request.method == 'POST':
        note.question          = request.POST.get('question', '').strip()
        note.answer            = request.POST.get('answer', '')
        note.question_type     = _resolve_type(request.POST)
        note.question_subtopic = request.POST.get('question_subtopic', '').strip()
        note.question_format   = request.POST.get('question_format', 'description')

        if request.FILES.get('attachment'):
            note.attachment = request.FILES.get('attachment')

        note.save()
        return redirect('home')

    return render(request, 'notes/edit_note.html', {
        'note':           note,
        'type_choices':   _build_type_choices(),
        'format_choices': QANote.QUESTION_FORMAT_CHOICES,
        'subtopics_json': json.dumps(QANote.QUESTION_SUBTOPICS),
    })


def delete_note(request, note_id):
    note = get_object_or_404(QANote, id=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'notes/delete_note.html', {'note': note})
