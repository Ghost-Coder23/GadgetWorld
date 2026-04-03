from django import forms

from .models import ContactSubmission


class ContactSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'topic', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'topic': forms.Select(),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us how we can help...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', '')
        self.fields['name'].widget.attrs['autocomplete'] = 'name'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['phone'].widget.attrs['autocomplete'] = 'tel'

    def clean_message(self):
        return self.cleaned_data['message'].strip()
