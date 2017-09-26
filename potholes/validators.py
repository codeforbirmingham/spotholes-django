from django.core.exceptions import ValidationError

def plus_one_minus_one_validator(value):
    
    if value != -1 and value != 1:
        
        raise ValidationError(
            ('%(value)s is not 1 or -1'),
            params = {'value': value},
            )
            
    