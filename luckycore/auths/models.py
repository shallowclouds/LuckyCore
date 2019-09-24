from django.db import models
import random
from django.contrib.auth.models import User as DjangoUser
from django.conf import settings
import requests
import json


str_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"


def generate_user_id(length=20):
    temp_id = str()
    for _ in range(length):
        temp_id += random.choice(str_set)
    return temp_id


class UserProfile(models.Model):

    # id = models.AutoField("id", primary_key=True)
    id = models.CharField("id", max_length=20, default=generate_user_id, primary_key=True)
    # username = models.CharField("username", max_length=100, default="lucky_son")
    score = models.IntegerField("score", default=0)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    token = models.CharField("token", max_length=100, default="")

    def check_score(self):
        pass

    def check_auth(self, password=""):
        url = settings.AUTH_URL
        data = dict(grant_type='password', username=self.user.username, password=password, expires_in=60)
        response = requests.post(url=url, data=data)
        if response.status_code != 200:
            info = str()
            if response.status_code == 400:
                info = "参数错误"
            if response.status_code == 404:
                info = "用户不存在"
            if response.status_code == 472:
                info = "用户被锁定"
            if response.status_code == 473:
                info = "用户名或密码错误"
            if response.status_code == 500:
                info = "Internal Server Error(指认证服务器)"
            return False, info
        else:
            data = json.loads(response.content)
            self.token = data["access_token"]
            return True, "认证成功"
