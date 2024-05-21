from django import template
from web import models
register = template.Library()


@register.filter
def highlight(num_type):
    style_mapping = models.TransactionRecord.charge_type_mapping
    return style_mapping.get(num_type)
