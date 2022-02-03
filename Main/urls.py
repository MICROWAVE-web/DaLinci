"""DaLinci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django_email_verification import urls as email_urls
from django.contrib.auth.views import LogoutView
from django.conf import settings

from .views import *  # optimize

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('reg/', CustomRegView.as_view(), name='registration'),
    path('sms_verification/<slug:user_pk>/', sms_verification, name='sms_verification'),
    path('service/', ServiceView.as_view(), name='service'),
    path('links/', LinksTableView.as_view(), name='links'),
    path('l/<slug:urlhash>/', LinkDetailView.as_view(), name='link'),
    path('count_chart/<slug:urlhash>/', count_chart, name='count_chart'),
    path('get_hash_link/', get_hash_link, name='get_hash_link'),
    path('email/', include(email_urls)),
    path('test/', test, name='test'),
    path('r/<slug:urlhash>/', link_redirect, name='redirect'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
