from .models import Tag, Note


def get_user_tag(user):
    return Tag.objects.filter(user=user).all()


def get_user_choice_tags(user, choice_tags_list):
    return Tag.objects.filter(user=user, name__in=choice_tags_list)


def get_user_notes(user):
    return Note.objects.filter(user=user).all()


def get_user_notes_with_tags(user, tags):
    return Note.objects.filter(user=user, tags__in=tags).distinct()


def set_done_user_note(user, note_id):
    Note.objects.filter(user=user, pk=note_id).update(done=True)


def delete_user_note(user, note_id):
    Note.objects.get(user=user, pk=note_id).delete()
