from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from rest_framework.exceptions import ValidationError

# ----------------------------------------------------------------------------------------------------------
def no_offensive_words(value):
    offensive_list = ['fuck', 'fucking', 'bitch', 'bastered']
    for word in value.split():
        if word.lower() in offensive_list:
            raise ValidationError(f"you are not allowed to use the word {word} because it's offensive.")
# ----------------------------------------------------------------------------------------------------------
class Review(models.Model):
    status_choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]

    # Generic Foreign Key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)         # real db field
    object_id = models.PositiveIntegerField()                                       # real db field
    content_object = GenericForeignKey('content_type', 'object_id')                 # virtual field

    # custom fields
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[no_offensive_words])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default='pending', null=False, blank=False, choices=status_choices)

    def __str__(self):
        return f"on {self.content_object} | by {self.review_user}"

# ----------------------------------------------------------------------------------------------------------
class CarAd(models.Model):
    city_choices = [('sanandaj', 'sanandaj'), ('tehran', 'tehran'), ('shiraz', 'shiraz'), ('boukan', 'boukan')]
    brand_choices = [('peugeot', 'peugeot'), ('renault', 'renault'), ('iran khodro', 'iran khodro'), ('saipa', 'saipa')]
    model_choices = [('206', '206'), ('405', '405'), ('pars', 'pars'),('l90', 'l90'), ('sandro', 'sandro'), ('duster', 'duster'),
                    ('samand', 'samand'), ('dena', 'dena'), ('tara', 'tara'),('shahin', 'shahin'), ('tiba', 'tiba'), ('saina', 'saina')]
    fuel_choices = [('gsoline', 'gasoline'), ('corporate dual fuel', 'corporate dual fuel'),
                    ('manual dual fuel', 'manual dual fuel'), ('diesel', 'diesel')]
    color_choices = [('white', 'white'), ('black','black'), ('gray', 'gray'), ('blue', 'blue')]
    body_choices = [('intact', 'intact'), ('minor scratches', 'minor scratches'), ('polished unpainted', 'polished unpainted'),
                    ('partially painted', 'partially painted'), ('mostly painted', 'mostly painted'), ('fully painted', 'fully painted'),
                    ('crashed', 'crashed'), ('scrapped', 'scrapped')]
    chassis_choices = [('intact', 'intact'), ('damaged', 'damaged'), ('painted', 'painted')]
    engine_choices = [('intact', 'intact'), ('needs repair', 'needs repair'), ('replaced', 'replaced')]
    gearbox_choices = [('manual', 'manual'), ('automatic', 'automatic')]
    status_choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]


    ad_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_ads')
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=50, choices=city_choices)
    brand = models.CharField(max_length=100, choices=brand_choices)
    model = models.CharField(max_length=50, choices=model_choices)
    mileage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    fuel_type = models.CharField(max_length=50, choices=fuel_choices)
    production_year = models.IntegerField(validators=[MinValueValidator(2001), MaxValueValidator(2025)])
    color = models.CharField(max_length=50, choices=color_choices)
    body_condition = models.CharField(max_length=50, choices=body_choices)
    front_chassis_condition = models.CharField(max_length=50, choices=chassis_choices)
    rear_chassis_condition = models.CharField(max_length=50, choices=chassis_choices)
    engine_condition = models.CharField(max_length=50, choices=engine_choices)
    gearbox = models.CharField(max_length=20, choices=gearbox_choices)
    third_party_insurance_period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    price = models.IntegerField()
    willing_to_exchange = models.BooleanField()
    description = models.CharField(max_length=1000)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in the format: 09xxxxxxxxx')])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default='pending', null=False, blank=False, choices=status_choices)
    reviews = GenericRelation(Review)

    def __str__(self):
        return f"{self.model} | {self.production_year}"

# ----------------------------------------------------------------------------------------------------------
class MotorcycleAd(models.Model):
    city_choices = [('sanandaj', 'sanandaj'), ('tehran', 'tehran'), ('shiraz', 'shiraz'), ('boukan', 'boukan')]
    brand_choices = [('apache', 'apache'), ('yamaha', 'yamaha'), ('honda', 'honda')]
    model_choices = [('a 160', 'a 160'), ('a 180', 'a 180'), ('a 200', 'a 200'),
                      ('yt 125', 'yt 125'), ('yt 250', 'yt 250'), ('yt 400', 'yt 400'),
                        ('hcb 150', 'hcb 150'), ('hcb 250', 'hcb 250'), ('hcb 300', 'hcb 300')]
    status_choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]

    
    ad_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='motorcycle_ads')
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=50, choices=city_choices)
    brand = models.CharField(max_length=100, choices=brand_choices)
    model = models.CharField(max_length=50, choices=model_choices)
    mileage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    production_year = models.IntegerField(validators=[MinValueValidator(2001), MaxValueValidator(2025)])
    price = models.IntegerField()
    willing_to_exchange = models.BooleanField()
    description = models.CharField(max_length=1000)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in the format: 09xxxxxxxxx')])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default='pending', null=False, blank=False, choices=status_choices)
    reviews = GenericRelation(Review)

    def __str__(self):
        return f"{self.model} | {self.production_year}"

# ----------------------------------------------------------------------------------------------------------

class CarAdImage(models.Model):
    status_choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]

    car_ad = models.ForeignKey(CarAd, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/', null=False, blank=False)
    # description = models.CharField(max_length=150, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='pending', null=False, blank=False, choices=status_choices)

# ----------------------------------------------------------------------------------------------------------

class MotorcycleAdImage(models.Model):
    status_choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]

    motorcycle_ad = models.ForeignKey(MotorcycleAd, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='motorcycle_images/', null=False, blank=False)
    # description = models.CharField(max_length=150, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='pending', null=False, blank=False, choices=status_choices)

# ----------------------------------------------------------------------------------------------------------




# /////////////////////////////////////////////  SIGNALS  ////////////////////////////////////////////
# ----------------------------------------------------------------------------------------------------------

# automate deleting the car ad images from the storage after deleting the CarAdImage instance using post_delete signal.
# This function listens to the deletion of any CarAdImage instance and deletes the corresponding image from disk.
# instance.image.path gives you the absolute path of the image file.
# This works only if MEDIA_ROOT is properly set in your settings.py.

from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

@receiver(post_delete, sender=CarAdImage)
def delete_car_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# ----------------------------------------------------------------------------------------------------------
# automate deleting the motorcycle ad images from the storage after deleting the MotorcycleAdImage instance using post_delete signal.

from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
@receiver(post_delete, sender=MotorcycleAdImage)
def delete_motorcycle_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
