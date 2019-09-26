from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.conf import settings


class LuckView(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        cxt = dict()
        userprofile = request.user.userprofile
        userprofile = dict(id=userprofile.id, score=userprofile.score, username=request.user.username)
        records_query = OpRecord.objects.filter(for_user=request.user).order_by('op_time')
        records = [dict(for_user=record.for_user.username,
                        by_user=record.by_user.username,
                        added_score=record.added_score,
                        op_time=record.op_time) for record in records_query]
        score = 0
        for record in records:
            score = score + record['added_score']
        userprofile['score'] = score
        activity = Activity.objects.order_by("max_score")[0]
        activity = dict(time_gap=activity.time_gap,
                        name=activity.name,
                        info=activity.info,
                        max_score=activity.max_score)
        cxt = dict(userprofile=userprofile, records=records, activity=activity)
        return render(request, "luck/luck.html", cxt)

    @method_decorator(login_required(login_url="login"))
    def post(self, request):
        return HttpResponse("qaq, {} got a misfortune.".format(request.user.username))


class ShareView(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, user_id):
        cxt = dict()
        try:
            userprofile = UserProfile.objects.all().get(id=user_id)
        except UserProfile.DoesNotExist:
            return render(request, "luck/error.html")
        records_query = OpRecord.objects.filter(for_user=userprofile.user).order_by('op_time')
        userprofile = dict(id=userprofile.id, score=userprofile.score, username=userprofile.user.username)
        records = [dict(for_user=record.for_user.username,
                        by_user=record.by_user.username,
                        added_score=record.added_score,
                        op_time=record.op_time) for record in records_query]
        score = 0
        for record in records:
            score = score + record['added_score']
        userprofile['score'] = score
        activity = Activity.objects.order_by("max_score")[0]
        activity = dict(time_gap=activity.time_gap,
                        name=activity.name,
                        info=activity.info,
                        max_score=activity.max_score)
        cxt = dict(userprofile=userprofile, records=records, activity=activity)
        return render(request, "luck/share.html", cxt)

    @method_decorator(login_required(login_url="login"))
    def post(self, request, user_id):
        cxt = dict()
        try:
            userprofile = UserProfile.objects.all().get(id=user_id)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('error'))
        records_query = OpRecord.objects.\
            filter(for_user=userprofile.user, by_user=request.user).\
            order_by('-op_time')
        activity = Activity.objects.order_by("max_score")[0]
        if len(records_query) == 0 or records_query[0].op_time + activity.time_gap < timezone.now():
            if userprofile.score >= activity.max_score:
                messages.info(
                    request,
                    "虽然 {} 的能量池快要溢出了，但要是让它散失了他会不高兴的=-=".format(userprofile.user.username)
                )
                return HttpResponseRedirect(reverse('share', args=(user_id, )))
            new_record = OpRecord.objects.create(
                activity=activity,
                for_user=userprofile.user,
                by_user=request.user,
                added_score=0
            )
            for _ in range(3):
                new_record.added_score = new_record.get_random_score(userprofile.score)
                if new_record.added_score > 0:
                    break
            new_record.save()
            userprofile.score = userprofile.score + new_record.added_score
            userprofile.save()
            messages.warning(request, "成功为 {username} 增加 {score} pt=-=".format(
                username=userprofile.user.username,
                score=new_record.added_score
            ))
            return HttpResponseRedirect(reverse('share', args=(user_id, )))
        else:
            messages.warning(request, "为 {} 注♂入能量的操作还在冷却中=-=".format(userprofile.user.username))
            return HttpResponseRedirect(reverse('share', args=(user_id, )))


def error_view(request):
    return render(request, "luck/error.html")


@login_required(login_url="login")
def flag_view(request):
    return HttpResponse("qaq")
