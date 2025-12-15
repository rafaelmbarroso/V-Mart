from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    bookmarks = models.ManyToManyField(
        "Listings",
        related_name="bookmarked_by",
        blank=True
    )

    def __str__(self):
        return self.username

class Listings(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    creation_Date = models.DateTimeField(auto_now_add=True)
    is_on_campus = models.BooleanField(default=False)


    #image upload 
    image = models.ImageField(
        upload_to='listing_images/', 
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
