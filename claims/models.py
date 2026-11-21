from django.db import models
from django.conf import settings
from items.models import Item
from django.contrib.auth.hashers import make_password, check_password



class Claim(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    lost_item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matched_claims'
    )

    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    verification_passed = models.BooleanField(default=False)

    verification_attempts = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    returned = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    received_at = models.DateTimeField(
        null=True,
        blank=True
    )

    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_handovers'
    )

    returned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    handover_notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.claimant} - {self.item.name}"


class VerificationQuestion(models.Model):

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='verification_questions'
    )

    question = models.CharField(max_length=255)

    answer_hash = models.CharField(max_length=128)

    def set_answer(self, answer):
        self.answer_hash = make_password(answer.strip().casefold())

    def check_answer(self, answer):
        return check_password(
            answer.strip().casefold(),
            self.answer_hash
        )

    def __str__(self):
        return f"{self.item.name} - {self.question}"
