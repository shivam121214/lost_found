
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'item_type',
            'name',
            'category',
            'description',
            'private_details',
            'image',
            'location',
            'date_of_occurrence',
        ]

        widgets = {
            'date_of_occurrence': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
