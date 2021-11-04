from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View


class CustomRegView(View):
    pass


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'center_text': 'Вход в личный кабинет',
        'title': 'DaLinci.com - Вход в личный кабинет'
    }


def test(request):
    return render(request, 'test.html')
