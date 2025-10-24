from django.db import models



# # Create your models here.
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')
    profile_image = models.ImageField(upload_to='profile_images/', default='default_img/avatar.jpg', blank=False, null=False)
    address_line = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=100, blank=False)
    pincode = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
