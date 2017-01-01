from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader import get_template

from django.views.generic.base import RedirectView, TemplateView

from enrollments.forms import SigninForm, UserForm, ProfileForm

# Create your views here.


def signin(request):
    context = {}
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if request.is_ajax():
            if form.is_valid():
                try:
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            context.update({'user': user})
                            dasboard_area = get_template(template_name="enrollments/dashboard.html")
                            html = dasboard_area.render(context)
                            return JsonResponse({'html': html}, status=200)
                except:
                    error_msg = "Something went wrong. Please try again later"
                    return JsonResponse({'error_msg': error_msg}, status=400)
            else:
                return JsonResponse(form.errors, status=400)

    else:
        # login form
        context['signin_form'] = SigninForm

        # for registering new employee
        context['user_form'] = UserForm
        context['profile_form'] = ProfileForm
        context['action_url'] = reverse('signin')

    return render(request, 'base.html', context)


def signout(request):
    logout(request)
    return redirect('go-to-signin')


def create_user_profile(request):
    pass


def update_user_profile(request):
    pass
