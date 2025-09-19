from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login as django_login
from django.urls import reverse

def sign_up(request):
    # 추가
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")

    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/signup.html", context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get("next")
        if next:
            return redirect(next)

        return redirect(reverse('blog:list'))

    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)
