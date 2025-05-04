from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, blank=True, null=True)
    family_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in the format: 09xxxxxxxxx')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.family_name}"



# signal to instantiate the Profile Instance with connecting it to the User model instance first.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
