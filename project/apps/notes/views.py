from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, NoteForm
from .models import Tag, Note


# Create your views here.
@login_required
def main(request):
    tags = Tag.objects.filter(user=request.user).all()
    choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
    if len(choice_tags) == 0:
        notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
        return render(request, 'notes/notes_list.html', context={'notes': notes, 'tags': tags})
    else:
        notes = Note.objects.filter(user=request.user,
                                    tags__in=choice_tags).distinct() if request.user.is_authenticated else []
        return render(request, 'notes/notes_list.html',
                      context={'notes': notes, 'tags': tags, 'choice_tags': request.POST.getlist('tags')})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
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
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            print(request.POST.getlist('tags'))
            for tag in choice_tags:
                note.tags.add(tag)

            return redirect(to="notes:main")
        else:
            return render(request, 'notes/add_note.html',  context={'form': form, 'tags': tags})

    return render(request, 'notes/add_note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notes/detail.html', context={"note": note})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to="notes:main")


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to="notes:main")
