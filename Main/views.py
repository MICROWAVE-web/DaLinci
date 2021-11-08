import django
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django_email_verification import send_email

from .forms import UserRegistrationForm, ServiceForm
from .models import AbbreviatedLink, Transition


class CustomRegView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
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


class ServiceView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'title': 'DaLinci.com',
            'form': ServiceForm()
        }
        return render(request, 'service/service.html', context)


def get_hash_link(request, *args, **kwargs):
    form = ServiceForm(request.POST)
    if form.is_valid():
        try:
            if not request.user.is_authenticated and AbbreviatedLink.objects.filter(parent_link=form.cleaned_data['parent_link'], owner__isnull=True).exists():
                print('1')
                abbrlink = AbbreviatedLink.objects.get(parent_link=form.cleaned_data['parent_link'], owner__isnull=True)
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'localhost:8000/r/{abbrlink.urlhash}',
                }
            elif not request.user.is_authenticated:
                print('2')
                abbrlink = form.save()
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'localhost:8000/r/{abbrlink.urlhash}',
                }
            else:
                print('3')
                abbrlink = form.save(commit=False)
                abbrlink.owner = request.user
                abbrlink = form.save()
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'localhost:8000/r/{abbrlink.urlhash}',
                }
            return JsonResponse(context)
        except django.db.utils.IntegrityError:
            context = {
                'error': 'You already have the same link!',
            }
            return JsonResponse(context)
    else:
        context = {
            'error': 'Form invalid!',
        }
        return JsonResponse(context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def link_redirect(request, urlhash):
    try:
        redirect_obj = AbbreviatedLink.objects.get(urlhash=urlhash)
        redirect_obj.counter += 1
        redirect_obj.save()
        transition = Transition(ip=get_client_ip(request), abbr_link=redirect_obj)
        transition.save()
        return HttpResponseRedirect(redirect_obj.parent_link)
    except AbbreviatedLink.DoesNotExist:
        return HttpResponseNotFound("404")


def test(request):
    return render(request, 'service/service.html')
