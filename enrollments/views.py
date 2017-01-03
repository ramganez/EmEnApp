from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.views.generic.base import RedirectView, TemplateView

from enrollments.models import Profile
from enrollments.forms import SigninForm, UserForm, ProfileForm, UserUpdateForm

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
                    if user is not None and user.is_active:
                        login(request, user)
                        context.update({'user': user})
                        dasboard_area = get_template(template_name="enrollments/dashboard.html")
                        html = dasboard_area.render(context)
                        return JsonResponse({'html': html, 'profile_url': user.profile.get_absolute_url()},
                                            status=200)
                except:
                    error_msg = "Something went wrong. Please try again later"
                    return JsonResponse({'form_errors': error_msg}, status=400)
            else:
                return JsonResponse({'form_errors': 'Incorrect username or password.'}, status=400)

    else:
        if request.user.is_authenticated():
            profile_obj = request.user.profile
            return redirect(profile_obj)
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
            # create user
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
            profile_obj = Profile.objects.create(user=user, date_of_birth=date_of_birth, years_of_experience=years_of_experience,
                                   designation=designation)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            context.update({'user': user})
            dasboard_area = get_template(template_name="enrollments/dashboard.html")
            html = dasboard_area.render(context)
            # json response with dashboard
            return JsonResponse({'html': html, 'profile_url': profile_obj.get_absolute_url()}, status=200)

        else:

            # for append profile errors as well
            profile_form.is_valid()

            form_errors = '<br>'.join(user_form.non_field_errors())
            for e in user_form.errors.values():  # [[u'Not valid format.'], [u'please check the detail .']]
                form_errors += '<br>' + e[0]

            form_errors += '<br>'.join(profile_form.non_field_errors())
            for e in profile_form.errors.values():  # [[u'Not valid format.'], [u'please check the detail .']]
                form_errors += '<br>' + e[0]

            return JsonResponse({'form_errors':form_errors}, status=400)

    else:
        return redirect('go-to-signin')


def update_user_profile(request, **kwargs):
    if request.user.is_authenticated():
        instance = get_object_or_404(User, id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=instance)
        profile_form = ProfileForm(request.POST or None, instance=instance.profile)
        if request.method == 'POST':
            if user_form.is_valid() and profile_form.is_valid():
                user_obj = user_form.save()
                user_obj.username = user_form.cleaned_data['username']
                user_obj.email = user_form.cleaned_data['username']
                profile_obj = profile_form.save()
                dasboard_area = get_template(template_name="enrollments/dashboard.html")
                html = dasboard_area.render({'user': user_obj})
                # json response with dashboard
                return JsonResponse({'html': html, 'profile_url': profile_obj.get_absolute_url()}, status=200)

            else:
                # for append profile errors as well
                profile_form.is_valid()

                form_errors = '<br>'.join(user_form.non_field_errors())
                for e in user_form.errors.values():  # [[u'Not valid format.'], [u'please check the detail .']]
                    form_errors += '<br>' + e[0]

                form_errors += '<br>'.join(profile_form.non_field_errors())
                for e in profile_form.errors.values():  # [[u'Not valid format.'], [u'please check the detail .']]
                    form_errors += '<br>' + e[0]

                return JsonResponse({'form_errors':form_errors}, status=400)

        return render(request, 'enrollments/update_profile_form.html',
                      {'update_action_url': request.user.profile.get_update_url(), 'user_form':user_form,
                       'profile_form':profile_form})
    else:
        return redirect('go-to-signin')


def dashboard_view(request, **kwargs):
    try:
        if request.user.is_authenticated():
            return render(request, 'enrollments/dashboard.html', {'user': request.user})
        else:
            return redirect('go-to-signin')
    except:
        raise Http404("<h1> Something went wrong !!!<h1>")
