from django.core.exceptions import ValidationError

def min_len_validator(value):
    if len(value) < 100:
        raise ValidationError('Description must be atleast 100 characters long!')