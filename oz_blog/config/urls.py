"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from django.conf.urls.static import static
from config import settings
from member import views as member_views
from django.urls import path, include
from django.views.generic import TemplateView, View

# 간단한 테스트 뷰
class AboutView(TemplateView):
    template_name = "about.html"

class TestView(View):
    def get(self, request):
        return render(request, "test.get.html")

    def post(self, request):
        return render(request, "test.post.html")


urlpatterns = [
    path("admin/", admin.site.urls),                 # 관리자 페이지
    path("", include("blog.urls")),                  # 블로그 앱을 루트('/')에 연결
    path("fb/", include("blog.fbv_urls")),           # FBV 기반 blog URL

    path("accounts/", include("django.contrib.auth.urls")),  # 로그인/로그아웃 기본 제공
    path("signup/", member_views.sign_up, name="signup"),
    path("login/", member_views.login, name="login"),

    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

