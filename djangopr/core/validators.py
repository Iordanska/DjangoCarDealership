from datetime import datetime, date

from django.core.exceptions import ValidationError


def date_validator(value):
    if value < date(1901, 1, 1) or value > date.today():
        raise ValidationError(
            _("%(value)s is not a correct date."),
            params={"value": value},
        )


def year_validator(value):
    if value < 1960 or value > datetime.now().year:
        raise ValidationError(
            _("%(value)s is not a correct year!"),
            params={"value": value},
        )
