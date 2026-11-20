from django.contrib import admin
from .models import Claim, VerificationQuestion


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'claimant',
        'status',
        'created_at',
    )

    list_filter = ('status',)
    search_fields = (
        'item__name',
        'claimant__email',
    )

    readonly_fields = ('created_at',)


@admin.register(VerificationQuestion)
class VerificationQuestionAdmin(admin.ModelAdmin):

    list_display = ('item', 'question')
    search_fields = ('item__name', 'question')