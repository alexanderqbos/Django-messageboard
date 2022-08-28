from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UpdateMessage(forms.Form):
    message = forms.CharField(min_length=1, max_length=160, strip=True)
    
    def clean_message(self):
        data = str(self.cleaned_data['message'])

        if len(data) == 1 and (data == ' ' or data == '\n'):
            raise ValidationError(_('Bad message length'))

        return data