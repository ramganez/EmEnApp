from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.views.generic.base import RedirectView, TemplateView

from enrollments.models import Profile
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
        context['signin_action_url'] = reverse('signin')
        context['reg_action_url'] = reverse('register')

    return render(request, 'base.html', context)


def signout(request):
    logout(request)
    return redirect('go-to-signin')


def create_user_profile(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['email']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']
            new_user.save()

            # create profile
            date_of_birth = profile_form.cleaned_data['date_of_birth']
            years_of_experience = profile_form.cleaned_data['years_of_experience']
            designation = profile_form.cleaned_data['designation']
            user = new_user
            Profile.objects.create(user=user, date_of_birth=date_of_birth, years_of_experience=years_of_experience,
                                   designation=designation)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            context.update({'user': user})
            dasboard_area = get_template(template_name="enrollments/dashboard.html")
            html = dasboard_area.render(context)
            return JsonResponse({'html': html}, status=200)

        else:
            return JsonResponse(profile_form.errors, status=400)



def update_user_profile(request):
    pass

