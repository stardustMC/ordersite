import json
from utils.response import BaseResponse
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class UserInfo:

    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role
        self.menu_name = None
        self.path_list = []


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info in settings.CRC_PUBLIC_URLS:
            return

        user_data = request.session.get(settings.CRC_USER_SESSION_KEY)
        if not user_data:
            return redirect(settings.CRC_LOGIN_URL)
        request.crc_user = UserInfo(**json.loads(user_data))

    def process_view(self, request, callback, callback_args, callback_kwargs):
        current_url = request.resolver_match.url_name
        if current_url in settings.CRC_COMMON_URLS:
            return

        user_data = request.crc_user
        permission_dict = settings.CRC_PERMISSION[user_data.role]
        if current_url not in permission_dict:
            if request.is_ajax():
                return BaseResponse(False, details="没有足够的权限").as_json()
            return redirect(reverse(viewname='denied'))

        current_path = permission_dict[current_url]
        while True:
            if '{}' in current_path['url']:
                current_path['url'] = current_path['url'].format(request.crc_user.id)
            user_data.path_list.append(current_path)
            parent = current_path['parent']
            if parent:
                current_path = permission_dict[parent]
            else:
                if current_url != 'home':
                    user_data.path_list.append(permission_dict['home'])
                break
        user_data.path_list.reverse()
        user_data.path_list[-1]['class'] = 'active'
        request.crc_user = user_data
