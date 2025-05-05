from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser (AbstractUser ):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', related_name='staff_members', null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['first_name', 'last_name']

class Report(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    id_proof = models.ImageField(upload_to='id_proofs/')  # Directory for uploaded images
    comment = models.TextField(blank=True, null=True)  # Optional field for comments/notes
    date = models.DateField(auto_now_add=True)  # Automatically set the field to now when the object is created
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # Set a default value if needed
    )
    staff = models.ForeignKey(CustomUser ,null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
    


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    link = models.URLField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

    

