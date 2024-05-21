import copy
from django import template
from django.conf import settings
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch

register = template.Library()


@register.inclusion_tag('menu.html')
def menu(request):
    path = request.path_info
    user_menu = copy.deepcopy(settings.CRC_MENU_DICT[request.crc_user.role])
    for item in user_menu:
        for child in item['children']:
            try:
                child['url'] = reverse(viewname=child['name'])
            except NoReverseMatch:
                child['url'] = reverse(viewname=child['name'], kwargs={'pk': request.crc_user.id})
            if child['url'] == path:
                child['class'] = 'chosen'
    return {
        'menu': user_menu
    }
