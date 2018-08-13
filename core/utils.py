from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder


def decode_id(string_id):
    try:
        original_id = force_text(uid_decoder(string_id))
        return original_id.split(':')[1]
    except (TypeError, ValueError, OverflowError, IndexError) as e:
        raise ValueError(e)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    
    return False
