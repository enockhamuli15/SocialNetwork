from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image
from django.urls import reverse
from Profile.models import Profile



class Logins(AbstractUser):
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Domains(models.Model):
    description = models.CharField(max_length=120)

    def __str__(self):
        return str(self.description)

class Posts(models.Model):
    description = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='myLikes')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='myComments')
    shares = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='myShares')
    image_attached = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name='Attach_picture')
    createdTime = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_info', auto_created=True)
    domain = models.ForeignKey(Domains, on_delete=models.CASCADE, related_name='domain_info')
    

    def __str__(self):
        return str(self.description)

    class Meta:
        ordering = ('-createdTime',)

    @property
    def num_likes(self):
        return self.likes.all().count()

    @property
    def num_comments(self):
        return self.comment_set.all().count()

    @property
    def num_shares(self):
        return self.shares.all().count()

    def save(self):
        super().save()

        img = Image.open(self.image_attached.path)

        if img.height > 550 or img.width > 550:
            output_size = (550,550)
            img.thumbnail(output_size)
            img.save(self.image_attached.path)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

LIKE_CHOICE = {
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
}


class Like(models.Model):
    user = models.ForeignKey(Logins, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICE, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)



class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, auto_created=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, auto_created= True)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)


class Networks(models.Model):
    users = models.ForeignKey(Logins, on_delete=models.CASCADE, related_name='user_network')

    def __str__(self):
        return str(self.users)
