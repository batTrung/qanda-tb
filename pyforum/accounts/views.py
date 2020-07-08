from django.contrib.auth import login
from django.shortcuts import redirect, render
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


@login_required
def profile(request):
    return render(
        request,
        "accounts/profile.html",
    )


@login_required
def settings(request):
    return render(
        request,
        "accounts/settings.html",
    )
