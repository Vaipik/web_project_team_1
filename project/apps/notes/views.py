from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.utils import IntegrityError

from .forms import TagForm, NoteForm
from .models import Tag, Note
from .services import get_user_tag, get_user_notes, get_user_choice_tags, get_user_notes_filter, set_done_user_note, \
    set_undone_user_note, delete_user_note, get_user_id_note, get_user_note_tags, unused_tags, delete_user_tag


# Create your views here.
@login_required
def main(request):
    tags = get_user_tag(request.user)
    choice_tags = get_user_choice_tags(request.user, request.POST.getlist('tags'))
    choice_done = request.POST.getlist('done_or_not')
    notes = get_user_notes_filter(user=request.user, choice_tags=choice_tags,
                                  choice_done=choice_done) if request.user.is_authenticated else []
    if request.method == 'POST':
        return render(request, 'notes/notes_list.html',
                      context={'notes': notes,
                               'tags': tags,
                               'choice_tags': request.POST.getlist('tags'),
                               'choice_done': choice_done})
    else:
        return render(request, 'notes/notes_list.html',
                      context={'notes': notes,
                               'tags': tags,
                               'choice_tags': [],
                               'choice_done': []})


@login_required
def add_tag(request):
    tags = get_user_tag(request.user)
    tags_for_remove = unused_tags(request.user)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                tag = form.save(commit=False)
                tag.user = request.user
                tag.name = str(tag.name).lower()
                tag.save()
            except IntegrityError:
                print(f'Tag {tag.name} already exist')
            finally:
                return redirect(to="notes:main")
        else:
            return render(request, 'notes/tag.html', context={'form': form, 'tags': tags})

    return render(request, 'notes/tag.html', context={'form': TagForm(), 'tags': tags, 'tags_for_remove': tags_for_remove})


@login_required
def add_note(request):
    # print(request.POST)
    tags = get_user_tag(request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = get_user_choice_tags(request.user, request.POST.getlist('tags'))
            for tag in choice_tags:
                note.tags.add(tag)
            return redirect(to="notes:main")
        else:
            return render(request, 'notes/add_note.html', context={'form': form, 'tags': tags})

    return render(request, 'notes/add_note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def edit_note(request, note_id):
    tags = get_user_tag(request.user)
    note = get_user_id_note(request.user, note_id)
    form = NoteForm({'name': note.name, 'description': note.description})
    note_tags = []
    tags_note = get_user_note_tags(request.user, note)
    for tag in tags_note:
        note_tags.append(tag.name)
    return render(request, 'notes/edit_note.html', context={'form': form, 'tags': tags, 'note': note,
                                                            'note_tags': note_tags})


@login_required
def save_note(request, note_id):
    tags = get_user_tag(request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        note = get_user_id_note(request.user, note_id)
        if form.is_valid():
            note.name = request.POST['name']
            note.description = request.POST['description']
            choice_tags = get_user_choice_tags(request.user, request.POST.getlist('tags'))
            note.tags.set(choice_tags)
            note.save()
            return redirect(to="notes:main")
        else:
            note_tags = []
            tags_note = get_user_note_tags(request.user, note)
            for tag in tags_note:
                note_tags.append(tag.name)
            return render(request, 'notes/edit_note.html', context={'form': form, 'tags': tags, 'note': note,
                                                                    'note_tags': note_tags})

    return render(request, 'notes/add_note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def detail(request, note_id):
    tags = get_user_tag(request.user)
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notes/detail.html', context={"note": note, 'tags': tags})


@login_required
def set_done(request, note_id):
    set_done_user_note(request.user, note_id)
    return redirect(to="notes:main")


@login_required
def set_undone(request, note_id):
    set_undone_user_note(request.user, note_id)
    return redirect(to="notes:main")


@login_required
def delete_note(request, note_id):
    delete_user_note(request.user, note_id)
    return redirect(to="notes:main")


@login_required
def delete_tag(request):
    tags_for_remove = request.POST.getlist('tags_for_remove')
    for tag_name in tags_for_remove:
        delete_user_tag(request.user, tag_name)
    return redirect(to="notes:main")
