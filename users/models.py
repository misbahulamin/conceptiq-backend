from django.db import models
from django.contrib.auth.models import User

def profile_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    USER_ROLES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    bio = models.TextField()

    def __str__(self):
        return self.user.username