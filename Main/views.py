from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View
from django_email_verification import send_email
from .forms import UserRegistrationForm


class CustomRegView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email(user)
            context = {
                'replaceMessage': 'Подтверждение регистрации отправлено на почту '
                               f'{form.cleaned_data["email"]}',
                'title': 'DaLinci.com - Регистрация'
            }
            return render(request, 'authentication/go_mail.html', context)
        else:
            context = {
                'center_text': 'Регистрация',
                'title': 'DaLinci.com - Регистрация',
                'button_text': 'Продолжить',
                'form': form
            }
            return render(request, 'authentication/login.html', context)

    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'center_text': 'Регистрация',
            'title': 'DaLinci.com - Регистрация',
            'button_text': 'Продолжить',
            'form': UserRegistrationForm()
        }
        return render(request, 'authentication/login.html', context)


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'center_text': 'Вход в личный кабинет',
        'button_text': 'Войти',
        'title': 'DaLinci.com - Вход в личный кабинет'
    }


def test(request):
    return render(request, 'test.html')
