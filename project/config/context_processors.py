from apps.user_auth.forms import SignInAjaxForm, SignOutAjaxForm


def get_context(request):

    context = {
        "login_ajax": SignInAjaxForm(),
        "logout_ajax": SignOutAjaxForm(),
    }

    return context
