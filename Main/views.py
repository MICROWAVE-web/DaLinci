import datetime

import django
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django_email_verification import send_email
from django_tables2 import RequestConfig

from .forms import UserRegistrationForm, ServiceForm, SMSForm
from .models import AbbreviatedLink, Transition, User
from .tables import AbbreviatedLinkTable, TransitionTable
from .utils import MessageClient


class CustomRegView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user = form.save()
            if form.cleaned_data['type_of_confirmation'] == 'sms':
                mc = MessageClient()
                mc.send_message(
                    body=f"DaLinci.com. Verification code - {user.personal_sms_code}. "
                         "Thank you for using our service! ♥",
                    to=str(form.cleaned_data['phone']))
                context = {
                    'title': 'DaLinci.com - Registration',
                    'center_text': f'Phone number confirmation - {form.cleaned_data["phone"]}',
                    'button_text': 'Confirm',
                    'form': SMSForm(),
                    'user_pk': user.pk,
                }
                return render(request, 'authentication/sms_verification.html', context)
            else:
                send_email(user)
                context = {
                    'replaceMessage': 'Confirmation of registration has been sent by email '
                                      f'{form.cleaned_data["email"]}',
                    'title': 'DaLinci.com - Registration'
                }
                return render(request, 'authentication/go_mail.html', context)
        else:
            context = {
                'center_text': 'Registration',
                'title': 'DaLinci.com - Registration',
                'button_text': 'Продолжить',
                'form': form
            }
            return render(request, 'authentication/reg.html', context)

    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'center_text': 'Registration',
            'title': 'DaLinci.com - Registration',
            'button_text': 'Continue',
            'form': UserRegistrationForm()
        }
        return render(request, 'authentication/reg.html', context)


def sms_verification(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if not user:
        return HttpResponseNotFound
    form = SMSForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['personal_sms_code'] == user.personal_sms_code:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('service')
        else:
            context = {
                'title': 'DaLinci.com - Registration',
                'center_text': f'Phone number confirmation - {form.cleaned_data["phone"]}',
                'button_text': 'Continue',
                'form': SMSForm(),
                'user_pk': user_pk,
            }
            return render(request, 'authentication/sms_verification.html', context)


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'center_text': 'Login to your personal account',
        'button_text': 'Login',
        'title': 'DaLinci.com - Login to your personal account'
    }


class ServiceView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'title': 'DaLinci.com',
            'form': ServiceForm()
        }
        return render(request, 'service/service.html', context)


class LinksTableView(View):
    @staticmethod
    @login_required
    def get(request, *args, **kwargs):
        data = AbbreviatedLink.objects.filter(owner__email=request.user.email)
        table = AbbreviatedLinkTable(data, template_name='django_tables2/semantic.html')
        RequestConfig(request, paginate={"per_page": 15}).configure(table)
        context = {
            'title': 'DaLinci.com',
            'table': table
        }
        return render(request, 'service/links_table.html', context)


class LinkDetailView(View):
    @staticmethod
    @login_required
    def get(request, urlhash, *args, **kwargs):
        data = AbbreviatedLink.objects.get(owner__email=request.user.email, urlhash=urlhash)
        transitions = Transition.objects.filter(abbr_link_id=data.pk)
        table = TransitionTable(transitions, template_name='django_tables2/semantic.html')
        RequestConfig(request, paginate={"per_page": 15}).configure(table)
        context = {
            'title': 'DaLinci.com',
            'urlhash': urlhash,
            'link_data': data,
            'transitions': table
        }
        return render(request, 'service/detail_link.html', context)


def count_chart(request, urlhash, *args, **kwargs):
    labels = []
    data_chart = []
    data = AbbreviatedLink.objects.get(owner__email=request.user.email, urlhash=urlhash)
    for day in reversed(range(0, 8)):
        day_date = timezone.now() - datetime.timedelta(days=day)
        transitions = Transition.objects.filter(abbr_link_id=data.pk, time_and_date__date=day_date).count()
        # print(f'{day} - дней назад')
        # print(f'{day_date:"%Y-%m-%d"}')
        # print(f'{transitions} - количество переходов')
        labels.append(f'{day_date:"%Y-%m-%d"}')
        data_chart.append(transitions)
    # print(data_chart)
    return JsonResponse(data={
        'labels': labels,
        'data': data_chart,
    })


def get_hash_link(request, *args, **kwargs):
    form = ServiceForm(request.POST)
    if form.is_valid():
        try:
            if not request.user.is_authenticated and AbbreviatedLink.objects.filter(
                    parent_link=form.cleaned_data['parent_link'], owner__isnull=True).exists():
                abbrlink = AbbreviatedLink.objects.get(parent_link=form.cleaned_data['parent_link'],
                                                       owner__isnull=True)
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'dalinci.herokuapp.com/r/{abbrlink.urlhash}',
                }
            elif not request.user.is_authenticated:
                abbrlink = form.save()
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'dalinci.herokuapp.com/r/{abbrlink.urlhash}',
                }
            else:
                abbrlink = form.save(commit=False)
                abbrlink.owner = request.user
                abbrlink = form.save()
                context = {
                    'title': 'DaLinci.com',
                    'abbrlink': f'dalinci.herokuapp.com/r/{abbrlink.urlhash}',
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


def link_delete(request, urlhash):
    redirect_obj = AbbreviatedLink.objects.get(urlhash=urlhash)
    redirect_obj.delete()
    return redirect('links')


def page_not_found_view(request, exception):
    return render(request, 'exception/404.html', status=404)
