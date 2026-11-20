
from django.db import models
from django.conf import settings


class Item(models.Model):

    ITEM_TYPE_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('DOCUMENTS', 'Documents'),
        ('ACCESSORIES', 'Accessories'),
        ('CLOTHING', 'Clothing'),
        ('OTHER', 'Other'),
    ]

    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    private_details = models.TextField(
    blank=True,
    help_text="Private identifying details. Never displayed publicly."
    )
    location = models.CharField(max_length=200)
    date_of_occurrence = models.DateField()

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type} - {self.name}"
