from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import ProfileForm
from .models import Profile
from .services import get_profile_context


@login_required
def profile(request):
    context = get_profile_context(user=request.user)
    return render(request, "user_profile/profile.html", context)


class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = "user_profile/edit_profile.html"
    success_url = reverse_lazy("user_profile:profile")

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
