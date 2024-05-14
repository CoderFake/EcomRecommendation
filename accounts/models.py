import requests
from django.db import models
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils import timezone

from store.models import Product
from category.models import CategoryMain, SubCategory
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


def get_locations(id, parent_id):
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"
    if parent_id:
        api_url += f"&addressId={parent_id}"
    response = requests.get(api_url)
    locations = response.json().get('module', [])
    for location in locations:
        if location.get('id') == id:
            return location.get('name')
    return None
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=50, blank=True)

    # required fields for AbstractBaseUser
    date_joined = models.DateTimeField(auto_now_add=True)
    is_login = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=100, blank=True, default="Other")
    road = models.CharField(max_length=150, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.CharField(max_length=500, default="webapp/assets/images/user/user.png")
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.full_name

    def full_address(self):
        if self.road and self.ward and self.district and self.city:
            return self.road + ', ' + get_locations(self.ward, self.district) + ', ' + get_locations(self.district, self.city) + ', ' + get_locations(self.city, '')
        else:
            return ""

    def ward_name(self):
        if self.road and self.ward and self.district and self.city:
            return get_locations(self.ward, self.district)
        else:
            return ""

    def district_name(self):
        if self.road and self.ward and self.district and self.city:
            return get_locations(self.district, self.city)
        else:
            return ""

    def city_name(self):
        if self.road and self.ward and self.district and self.city:
            return get_locations(self.city, '')
        else:
            return ""



class EventUser(models.Model):
    EVENT_TYPES = (
        ('view', 'View'),
        ('cart', 'Cart'),
        ('pay', 'Pay'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_events')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_events')
    rating = models.IntegerField(default=0)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    frequency = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Event User'
        verbose_name_plural = 'Event Users'

    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.product.name}"

