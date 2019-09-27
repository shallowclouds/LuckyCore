from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User as DjangoUser
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.conf import settings


def dont_login(user):
    if user.is_authenticated:
        return False
    return True


class LoginView(View):

    def get(self, request):
        return render(request, "auths/login.html")

    @method_decorator(user_passes_test(dont_login, login_url="luck", redirect_field_name=""))
    def post(self, request):
        if "username" in request.POST and "password" in request.POST:
            try:
                user = DjangoUser.objects.all().get(username=request.POST["username"])
                auth_res, info = user.userprofile.check_auth(request.POST["password"])
                if auth_res:
                    auth_res = auth.authenticate(
                        request,
                        username=request.POST["username"],
                        password=settings.DEFAULT_PASSWORD)
                    auth.login(request, auth_res)
                    user.userprofile.save()
                    messages.info(request, info)
                    return HttpResponseRedirect(reverse("luck"))
                else:
                    messages.warning(request, info)
                    return HttpResponseRedirect(reverse("login"))
            except DjangoUser.DoesNotExist:
                user = DjangoUser(username=request.POST["username"], password=settings.DEFAULT_PASSWORD)
                user_profile = UserProfile(user=user)
                auth_res, info = user_profile.check_auth(request.POST["password"])
                if auth_res:
                    user = DjangoUser.objects.create_user(username=request.POST["username"],
                                                          password=settings.DEFAULT_PASSWORD)
                    UserProfile.objects.create(user=user)
                    auth_res = auth.authenticate(request,
                                                 username=request.POST["username"],
                                                 password=settings.DEFAULT_PASSWORD)
                    if auth_res is not None:
                        auth.login(request, auth_res)
                        messages.info(request, info)
                        return HttpResponseRedirect(reverse("luck"))
                    else:
                        messages.warning(request, "unknown error")
                        return HttpResponseRedirect(reverse("login"))
                else:
                    messages.warning(request, info)
                    return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "unknown error")
            return HttpResponseRedirect(reverse("login"))
