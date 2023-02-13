from .models import Tag, Note


def get_user_tag(user):
    return Tag.objects.filter(user=user).all()


def get_user_choice_tags(user, choice_tags):
    return Tag.objects.filter(user=user, name__in=choice_tags)


def get_user_note_tags(user, note):
    return Tag.objects.filter(user=user, tags_as_note=note)


def get_user_notes(user):
    return Note.objects.filter(user=user).all()


def get_user_id_note(user, note_id):
    return Note.objects.filter(user=user, pk=note_id).first()


def get_user_notes_filter(user, choice_tags=None, choice_done=None):
    notes = Note.objects.filter(user=user).distinct()
    if len(choice_tags) > 0:
        notes = notes.filter(tags__in=choice_tags)
    if 'done' in choice_done and not ('not done' in choice_done):
        notes = notes.filter(done=True)
    elif not('done' in choice_done) and ('not done' in choice_done):
        notes = notes.filter(done=False)
    return notes.distinct()


def set_done_user_note(user, note_id):
    Note.objects.filter(user=user, pk=note_id).update(done=True)


def set_undone_user_note(user, note_id):
    Note.objects.filter(user=user, pk=note_id).update(done=False)


def delete_user_note(user, note_id):
    Note.objects.get(user=user, pk=note_id).delete()


def unused_tags(user):
    notes = get_user_notes(user)
    tags = Tag.objects.filter(user=user).all()
    tags = tags.exclude(tags_as_note__in=notes)
    return tags


def delete_user_tag(user, tag_name):
    Tag.objects.get(user=user, name=tag_name).delete()
