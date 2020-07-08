from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

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
