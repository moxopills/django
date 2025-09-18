from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login as django_login
from django.urls import reverse

def sign_up(request):
    # 추가
    if request.method == "POST":  # POST 요청 시
        form = UserCreationForm(request.POST)  # 요청된 폼을 form에 받습니다.

        # form에 받은 데이터를 검증합니다
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")

    else:  # GET 요청 시 Form 새로 생성
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

        return redirect(reverse('blog_list')) # url을 찾는 reverse함수와 urls.py에 적은 name을 활용해 동적으로 작성

    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)
