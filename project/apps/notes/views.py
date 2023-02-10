from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, NoteForm
from .models import Tag, Note
from .services import get_user_tag, get_user_notes, get_user_choice_tags, get_user_notes_with_tags, set_done_user_note, \
    delete_user_note


# Create your views here.
@login_required
def main(request):
    tags = get_user_tag(request.user)
    choice_tags = get_user_choice_tags(request.user, request.POST.getlist('tags'))
    if len(choice_tags) == 0:
        notes = get_user_notes(request.user) if request.user.is_authenticated else []
        return render(request, 'notes/notes_list.html', context={'notes': notes, 'tags': tags})
    else:
        notes = get_user_notes_with_tags(request.user, choice_tags) if request.user.is_authenticated else []
        return render(request, 'notes/notes_list.html',
                      context={'notes': notes, 'tags': tags, 'choice_tags': request.POST.getlist('tags')})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.name = str(tag.name).lower()
            tag.save()
            return redirect(to="notes:main")
        else:
            return render(request, 'notes/tag.html', context={'form': form})

    return render(request, 'notes/tag.html', context={'form': TagForm()})


@login_required
def add_note(request):
    tags = Tag.objects.filter(user=request.user).all()

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
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notes/detail.html', context={"note": note})


@login_required
def set_done(request, note_id):
    set_done_user_note(request.user, note_id)
    return redirect(to="notes:main")


@login_required
def delete_note(request, note_id):
    delete_user_note(request.user, note_id)
    return redirect(to="notes:main")
