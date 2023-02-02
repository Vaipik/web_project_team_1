from .user_auth.forms import SignInForm


def get_context(request):

    context = {}

    if not request.user.is_authenticated:
        context.update({"login_ajax": SignInForm()})

    return context
