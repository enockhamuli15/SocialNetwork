from django.db import models
from django.conf import settings
from PIL import Image
from django.shortcuts import reverse
from django.db.models import Q
from django.template.defaultfilters import slugify
# Create your models here.


class ProfileManager(models.Manager):
    
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        query = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(query)

        accepted = set([])
        for rel in query:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField('SoftWord.Logins', on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='images/', default='images/defaultUser.png',
                                      verbose_name='Profile picture')
    description = models.CharField(default='...', max_length=250)
    dateOfBirth = models.DateField(blank=True, null=True, verbose_name='Date of Birth', default='1900-01-01')
    phoneNum = models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone number', default='+243000000000')
    friends = models.ManyToManyField('SoftWord.Logins', blank=True, default=None, related_name='friends')
    updated = models.DateTimeField(auto_now_add=True, auto_created=True)
    slug = models.SlugField(unique=True, blank=True)
    """ domain_id = models.ForeignKey(Domains, on_delete=models.CASCADE, related_name='domain_info_profile')
        """
    objects = ProfileManager()

    def __str__(self):
        return f'{ self.user.first_name} { self.user.last_name}'
    
    def get_absolute_url(self):
        return reverse("profile_detail_view", kwargs={"slug": self.slug})
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()
    
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.author_info.all()
        total_liked = 0
        for item in posts:
            total_liked += item.likes.all().count()
        return total_liked

    def get_posts_no(self):
        return self.author_info.all().count()

    def get_all_authors_posts(self):
        return self.author_info.all()
    
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.user.first_name
        self.__initial_last_name = self.user.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.user.first_name != self.__initial_first_name or self.user.last_name != self.__initial_last_name or self.slug=="":
            if self.user.first_name and self.user.last_name:
                to_slug = slugify(str(self.user.first_name) + " " + str(self.user.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        
        #######################
        img = Image.open(self.profile_photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)

        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        query = Relationship.objects.filter(receiver=receiver, status='send')
        return query

class Relationship(models.Model):
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True, auto_created=True)
    created = models.DateTimeField(auto_now_add=True, auto_created=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"