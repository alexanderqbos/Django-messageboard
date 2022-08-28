from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

KEY_LENGTH = 8
MSG_LENGTH = 160

#
# PURPOSE
# Validates that a key is alphanumeric
#
# PARAMETERS
# The key to be validated
#
# ERRORS/NOTES
# Raises a ValidationError if the key is not alphanumeric
#
def validate_key(value):
    if not value.isalnum():
        raise ValidationError('Key must be alphanumeric', code='key_val_error')

#
# PURPOSE
# Represents the message model consisting of a unique key and a message
#
# ERRORS/NOTES
# Keys must be alphanumeric and unique and of length KEY_LENGTH
# Messages must be of a length in range [1, 160]
#
class Message(models.Model):
    key = models.CharField(max_length=KEY_LENGTH, validators=[MinLengthValidator(KEY_LENGTH), MaxLengthValidator(KEY_LENGTH), validate_key])
    message = models.CharField(max_length=MSG_LENGTH, validators=[MinLengthValidator(1), MaxLengthValidator(MSG_LENGTH)])

#
# PURPOSE
# Converts the current message instance to string format
#
# PARAMETERS
# N/A
#
# ERRORS/NOTES
# N/A
#
    def __str__(self):
        return self.key + ': ' + self.msg

#
# PURPOSE
# Validates that the message key is unique
#
# PARAMETERS
# N/A
#
# ERRORS/NOTES
# Raises a ValidationError if the message key is not unique
#
    def clean(self):
        super().clean()
        msg = Message.objects.filter(key=self.key)
        if (len(msg) >= 1 and self.id == None): # QuerySet is empty if message key does not exist
            raise ValidationError('Message already exists', code='duplicate')
