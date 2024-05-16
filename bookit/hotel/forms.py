from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    age = forms.IntegerField(label=_('Age'))
    country = forms.CharField(max_length=100)
    photo = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15)

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        age = self.cleaned_data['age']
        country = self.cleaned_data['country']
        photo = self.cleaned_data['photo']
        phone_number = self.cleaned_data['phone_number']

        if hasattr(user, 'userprofile'):
            profile = user.userprofile
        else:
            profile = UserProfile(user=user)

        profile.first_name = first_name
        profile.last_name = last_name
        profile.age = age
        profile.country = country
        profile.photo = photo
        profile.phone_number = phone_number
        profile.save()

        return user
