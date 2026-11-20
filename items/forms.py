
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'item_type',
            'name',
            'contact_number',
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

def clean(self):
    cleaned_data = super().clean()

    item_type = cleaned_data.get('item_type')
    private_details = cleaned_data.get('private_details')
    contact_number = cleaned_data.get('contact_number')

    if not contact_number:
        self.add_error(
            'contact_number',
            'Contact number is required.'
        )

    if item_type == 'FOUND' and not private_details:
        self.add_error(
            'private_details',
            'Private identifying details are required for FOUND items.'
        )

    return cleaned_data
