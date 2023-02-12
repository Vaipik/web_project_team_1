from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import get_profile_context


@login_required
def profile(request):
    context = get_profile_context(user=request.user)

    return render(request, "user_profile/profile.html", context)
