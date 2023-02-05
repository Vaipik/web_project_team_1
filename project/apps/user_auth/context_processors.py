from .forms import SignInForm


def get_context(request):

    context = {
        "login_ajax": SignInForm(),
    }

    return context
