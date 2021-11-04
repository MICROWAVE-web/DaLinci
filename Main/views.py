from django.contrib.auth.views import LoginView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = ''


def test(request):
    return render(request, 'test.html')
