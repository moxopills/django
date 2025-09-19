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
from django.shortcuts import redirect, render
from blog import views
from member import views as member_views
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.views import View
from blog import cb_views


class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(View):
    def get(self,request):
        return render(request,'test.get.html')
    def post(self,request):
        return render(request,'test.post.html')

urlpatterns = [
    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),
]
