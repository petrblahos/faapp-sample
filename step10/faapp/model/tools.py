from formalchemy.exceptions import ValidationError
from formalchemy.validators import integer


def even(value, field=None):
    """
        Successful if the value is even.
    """
    value = integer(value, field)
    if value is None:
        return None
    if value % 2:
        try:
            _ = field.parent.active_request.translate
        except:
            _ = lambda x: x
        raise ValidationError(_('Value is not even'))
    return value

