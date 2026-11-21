
from django import forms
from .models import Claim, VerificationQuestion
from items.models import Item


class ClaimForm(forms.ModelForm):

    lost_item = forms.ModelChoiceField(
        queryset=Item.objects.none(),
        required=True,
        empty_label="Select your matching LOST report",
        label="Your Lost Report"
    )

    class Meta:
        model = Claim
        fields = ['lost_item']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['lost_item'].queryset = Item.objects.filter(
                reported_by=user,
                item_type='LOST'
            ).order_by('-created_at')


class VerificationQuestionForm(forms.ModelForm):

    answer = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        help_text="Enter the correct answer based on the item's private identifying details."
    )

    class Meta:
        model = VerificationQuestion
        fields = ['question', 'answer']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_answer(self.cleaned_data['answer'])

        if commit:
            instance.save()

        return instance


class ClaimVerificationForm(forms.Form):

    def __init__(self, *args, questions, **kwargs):
        super().__init__(*args, **kwargs)

        self.questions = questions

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.question,
                max_length=255,
                required=True
            )

    def answers_correct(self):
        results = [
            question.check_answer(
                self.cleaned_data[f'question_{question.id}']
            )
            for question in self.questions
        ]

        return all(results)
