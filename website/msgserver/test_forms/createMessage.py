from django import forms
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

class CreateMessage(forms.Form):
    key = forms.CharField(max_length=8, min_length=8, strip=True)
    message = forms.CharField(min_length=1, max_length=160, strip=True)

    def clean_key(self):
        data = str(self.cleaned_data['key'])

        data_len = len(data)
        
        if not data.isalnum():
            raise ValidationError(_('Invalid Key Entered!'))

        if data_len < 8 or data_len > 8:
            raise ValidationError(_('Invalid Key Entered!'))
    
    def clean_message(self):
        data = str(self.cleaned_data['message'])

        if len(data) == 1 and (data == ' ' or data == '\n'):
            raise ValidationError(_('Invalid Message - Enter a non-blank character!'))

        return data
