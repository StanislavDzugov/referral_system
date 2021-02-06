import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from user_profile import forms
from user_profile.models import UserProfile
from django.contrib.auth.decorators import login_required
from user_profile.models import CustomUser


def register_view(request):
    """Register new user"""

    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = request.POST.get('phone_number')
            request.session.set_expiry(60)
            return redirect('confirmation')
        else:
            messages.info(request, form.errors)
    else:
        form = forms.CreateUserForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def get_sms_from_center():
    """Getting sms from center"""
    code = get_random_string(length=6)
    # some logic to get_code
    return code


def phone_confirmation_view(request):
    """Login after code confirmation"""

    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        # code = request.POST.get('code') - get code from user, but we use our own to fit created code
        code = get_sms_from_center()  # - code which is user received from center
        own_code = code  # - code which we get from center
        if code == own_code:
            try:
                user, created = CustomUser.objects.get_or_create(phone_number=request.session['phone_number'])
            except:
                return HttpResponse("Session expired")
            user = authenticate(request, phone_number=user.phone_number)
            login(request, user)
            request.session['code'] = code
            time.sleep(2)
            return redirect('profile')
        else:
            messages.info(request, 'Code is incorrect')
    return render(request, 'confirmation_page.html')


def userlogout(request):
    """Logout session"""

    logout(request)
    return redirect('register')


@login_required(login_url='register')
def profile_view(request):
    """Profile page"""

    user_profile = UserProfile.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        referral_code = request.POST.get('invite')
        if UserProfile.objects.filter(user_referral_code=referral_code)\
                .exclude(user__id=request.user.id)\
                .exists():
            user_profile.activated_referral_code = referral_code
            user_profile.save()
            messages.success(request, 'You have successfully activate invite code ')
        else:
            messages.info(request, 'Wrong referral code')

    referral_users = UserProfile.objects\
        .filter(activated_referral_code=user_profile.user_referral_code)
    number_of_users = referral_users.count()
    context = {
        'user_profile': user_profile,
        'referral_users': referral_users,
        'number_of_users': number_of_users
    }
    return render(request, 'profile_page.html', context)


