from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import QANote


def _resolve_type(post_data):
    """
    If the user selected '__custom__' from the dropdown,
    use the text they typed in custom_type field instead.
    Normalises to lowercase-with-underscores so it can be
    used safely in CSS class names and URL params.
    """
    question_type = post_data.get('question_type', 'other')
    custom_type   = post_data.get('custom_type', '').strip()

    if question_type == '__custom__' and custom_type:
        # e.g. "Spring Boot" → "spring_boot"
        question_type = custom_type.lower().replace(' ', '_')[:50]
    elif not question_type or question_type == '__custom__':
        question_type = 'other'

    return question_type


def _build_type_choices():
    """
    Return predefined choices PLUS any custom types already stored in the DB.
    Custom types are discovered by querying distinct question_type values.
    """
    predefined = list(QANote.QUESTION_TYPE_CHOICES)
    predefined_keys = {v for v, _ in predefined}

    # Find custom types already saved in DB
    db_types = (
        QANote.objects
        .exclude(question_type__in=predefined_keys)
        .values_list('question_type', flat=True)
        .distinct()
        .order_by('question_type')
    )

    custom = [
        (t, t.replace('_', ' ').title())
        for t in db_types
        if t  # skip blank/null
    ]

    return predefined + custom


def home(request):
    if request.method == 'POST':
        question        = request.POST.get('question', '').strip()
        answer          = request.POST.get('answer', '').strip()
        question_type   = _resolve_type(request.POST)
        question_subtopic = request.POST.get('question_subtopic', '').strip()
        question_format = request.POST.get('question_format', 'description')
        attachment      = request.FILES.get('attachment')

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
    search_query    = request.GET.get('q', '')

    notes = QANote.objects.all()

    if filter_type:
        notes = notes.filter(question_type=filter_type)

    if filter_subtopic:
        notes = notes.filter(question_subtopic=filter_subtopic)

    if search_query:
        notes = notes.filter(question__icontains=search_query) | \
                notes.filter(answer__icontains=search_query)

    # Get current subtopics for the selected type
    current_subtopics = QANote.QUESTION_SUBTOPICS.get(filter_type, []) if filter_type else []

    # Pagination: 10 questions per page
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes/home.html', {
        'page_obj':            page_obj,
        'notes':               page_obj.object_list,
        'type_choices':        _build_type_choices(),
        'format_choices':      QANote.QUESTION_FORMAT_CHOICES,
        'subtopics':           QANote.QUESTION_SUBTOPICS,
        'current_subtopics':   current_subtopics,
        'filter_type':         filter_type,
        'filter_subtopic':     filter_subtopic,
        'search_query':        search_query,
    })


def edit_note(request, note_id):
    note = get_object_or_404(QANote, id=note_id)

    if request.method == 'POST':
        note.question        = request.POST.get('question', '').strip()
        note.answer          = request.POST.get('answer', '').strip()
        note.question_type   = _resolve_type(request.POST)
        note.question_subtopic = request.POST.get('question_subtopic', '').strip()
        note.question_format = request.POST.get('question_format', 'description')

        if request.FILES.get('attachment'):
            note.attachment = request.FILES.get('attachment')

        note.save()
        return redirect('home')

    return render(request, 'notes/edit_note.html', {
        'note':            note,
        'type_choices':    _build_type_choices(),
        'format_choices':  QANote.QUESTION_FORMAT_CHOICES,
        'subtopics':       QANote.QUESTION_SUBTOPICS,
    })


def delete_note(request, note_id):
    note = get_object_or_404(QANote, id=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'notes/delete_note.html', {'note': note})


@require_POST
def increment_read_count(request, note_id):
    """Increment the read count for a note (AJAX endpoint)"""
    note = get_object_or_404(QANote, id=note_id)
    note.read_count += 1
    note.save(update_fields=['read_count'])
    
    return JsonResponse({'read_count': note.read_count, 'success': True})
