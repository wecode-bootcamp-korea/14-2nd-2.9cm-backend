from django.db import models

from user.models import TimeStampModel

class Creator(TimeStampModel):
    username          = models.CharField(max_length=200)
    profile_image_url = models.URLField(max_length=2000)
    is_official       = models.BooleanField()
    user              = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'creators'

class Post(TimeStampModel):
    content_url  = models.URLField(max_length=2000)
    text_content = models.TextField()
    creator      = models.ForeignKey('Creator', on_delete=models.CASCADE)
    tag          = models.ManyToManyField('Tag', through='PostTag')

    class Meta:
        db_table = 'posts'

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'

class PostTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag  = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_tags'
