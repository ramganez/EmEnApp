from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from django.forms import ModelForm
from django import forms
from enrollments.models import Profile


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Please enter a correct username and password.")
            if not user.is_active:
                raise forms.ValidationError("User is no longer active.")
        return self.cleaned_data


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')

    email = forms.EmailField(max_length=64, help_text="The person's email address.")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Add all the fields you want a user to change
        fields = ('first_name', 'last_name', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'years_of_experience', 'designation')

