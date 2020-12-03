from pytz import timezone

from django.db import models
from django.conf import settings

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
