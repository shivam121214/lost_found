from django import forms
from .models import Claim, VerificationQuestion


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = []


class VerificationQuestionForm(forms.ModelForm):

    answer = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput
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
        return all(
            question.check_answer(
                self.cleaned_data[f'question_{question.id}']
            )
            for question in self.questions
        )
