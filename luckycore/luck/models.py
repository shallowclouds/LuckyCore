from django.db import models
from django.utils import timezone
from django.conf import settings
from auths.models import UserProfile, generate_user_id
from django.contrib.auth.models import User
import datetime
import random


class Flag(models.Model):

    id = models.AutoField("id", primary_key=True)
    flag = models.CharField("flag", max_length=200, default=generate_user_id)
    need_score = models.IntegerField("need_score", default=1000)

    def __str__(self):
        return str(self.flag)


class OpRecord(models.Model):

    id = models.AutoField("id", primary_key=True)
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    for_user = models.ForeignKey(User, related_name="for_user", on_delete=models.SET_NULL, null=True)
    by_user = models.ForeignKey(User, related_name="by_user", on_delete=models.SET_NULL, null=True)
    added_score = models.IntegerField("added_score", default=0)
    op_time = models.DateTimeField("op_time", default=timezone.now)

    def get_random_score(self, score=0):
        delta_score = int(random.normalvariate(settings.RANDOM_MU, settings.RANDOM_SIGMA))
        if score + delta_score > self.activity.max_score:
            delta_score = self.activity.max_score - score
        if score + delta_score < 0:
            delta_score = score
        return int(delta_score)

    def __str__(self):
        return str(self.by_user) + " to " + str(self.for_user)


class Activity(models.Model):

    id = models.AutoField("id", primary_key=True)
    time_gap = models.DurationField("time_gap", default=datetime.timedelta(days=1))
    name = models.CharField("name", max_length=100, default="You are the one chosen by the God!")
    info = models.CharField("info", max_length=1000, default="prove you are lucky enough and you'll get a flag.")
    max_score = models.IntegerField("max_score", default=settings.MAX_SCORE)

    def __str__(self):
        return str(self.name)
