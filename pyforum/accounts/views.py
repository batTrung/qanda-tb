from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


def profile(request, username):
    owner = get_object_or_404(get_user_model(), username=username)
    return render(
        request,
        "accounts/profile.html",
        {
            "owner": owner,
        }
    )


@login_required
def settings(request):
    return render(
        request,
        "accounts/settings.html",
    )
