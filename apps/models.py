from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CrimeReport(models.Model):
    THEFT = 'Theft'
    ASSAULT = 'Assault'
    VANDALISM = 'Vandalism'
    ROBBERY = 'Robbery'
    OTHER = 'Other'
    CRIME_TYPES = [
        (THEFT, 'Theft'),
        (ROBBERY, 'Robbery'),
        (ASSAULT, 'Assault'),
        (VANDALISM, 'Vandalism'),
        (OTHER, 'Other'),
    ]

    type_of_crime = models.CharField(max_length=50, choices=CRIME_TYPES, default=THEFT)
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    evidence = models.FileField(upload_to='evidence/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_number = models.CharField(max_length=20, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.report_number:
            self.report_number = f"{self.type_of_crime[:1].upper()}R-{timezone.now().strftime('%d%m%y-%H%M%S')}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.report_number + ' - ' + self.type_of_crime + ' - ' + self.location

# user profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='media/profile_pictures/', default='default.jpg', blank=True)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)  # New field for the title
    content = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)