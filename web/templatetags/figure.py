from django import template


register = template.Library()


@register.filter
def as_text(num, fix):
    try:
        num = int(num)
    except ValueError:
        return num

    if num < 10000:
        return num
    else:
        num = round(num / 10000, fix)
        return str(num) + '万'
