from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.CharField(max_length=4, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    # Add unique related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="cms_user_groups",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="cms_user_permissions",  # Unique related_name
        related_query_name="user",
    )

    def save(self, *args, **kwargs):
        if not self.user_id:
            last_user = User.objects.order_by('-user_id').first()
            if last_user:
                self.user_id = str(int(last_user.user_id) + 1).zfill(4)
            else:
                self.user_id = '1000'
        super().save(*args, **kwargs)