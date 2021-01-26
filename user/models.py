import sys, os, hmac, base64, requests, time, hashlib, json
from pytz import timezone

from django.db   import models
from django.conf import settings

from my_settings import NCP_ACCESS_KEY, NCP_SECRET_KEY, NCP_SERVICE_ID
from .api_urls   import SMS_API, SMS_URI

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.created_at.astimezone(korean_timezone)

    @property
    def updated_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.updated_at.astimezone(korean_timezone)

    class Meta:
        abstract = True

class User(TimeStampModel):
    email    = models.EmailField()
    password = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'

class UserDetail(TimeStampModel):
    name    = models.CharField(max_length=200, null=True)
    phone   = models.CharField(max_length=100, null=True)
    dob     = models.DateField(null=True)
    gender  = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=2000, null=True)
    user    = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_details'

class BrandLike(models.Model):
    brand = models.ForeignKey('store.Brand', on_delete=models.CASCADE)
    user  = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'brand_likes'

class ProductLike(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_likes'

class PostLike(models.Model):
    post = models.ForeignKey('tv.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_likes'

class PhoneAuth(TimeStampModel):
    phone       = models.CharField(max_length=100)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'phone_auths'

    def make_signature(self, message):
        SECRET_KEY = bytes(NCP_SECRET_KEY, 'UTF-8')

        return base64.b64encode(hmac.new(SECRET_KEY, message, digestmod=hashlib.sha256).digest())

    def send_message(self):
        timestamp = str(int(time.time() * 1000))

        message = "POST " + SMS_URI + "\n" + timestamp + "\n" + NCP_ACCESS_KEY
        message = bytes(message, 'UTF-8')

        SIGNATURE = self.make_signature(message)

        headers = {
            'Content-Type'             : 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp'    : timestamp,
            'x-ncp-iam-access-key'     : NCP_ACCESS_KEY,
            'x-ncp-apigw-signature-v2' : SIGNATURE
        }

        body = {
            "type"        : "SMS",
            "contentType" : "COMM",
            "from"        : "01028833153",
            "content"     : f'[2.9cm] 인증번호 [{self.auth_number}]를 입력해주세요.',
            "messages"    : [{ "to" : self.phone}]
        }

        result = requests.post(SMS_API, data = json.dumps(body), headers = headers).json()

        return result
