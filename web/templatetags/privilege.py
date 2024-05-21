from django import template
from django.conf import settings
from django.http import QueryDict
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def add_privilege(request, name, *args, **kwargs):
    role = request.crc_user.role

    permission_dict = settings.CRC_PERMISSION[role]
    if name not in permission_dict:
        return ""

    url = reverse(viewname=name, args=args, kwargs=kwargs)
    html = """<a href="{}">
            <button type="button" id="add-btn" class="btn btn-outline-success">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle"
                viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
            </svg>新 增</button></a>
            """.format(url)
    return mark_safe(html)


@register.simple_tag
def edit_privilege(request, name, *args, **kwargs):
    role = request.crc_user.role

    permission_dict = settings.CRC_PERMISSION[role]
    if name not in permission_dict:
        return ""

    params = request.GET.urlencode()
    key_dict = QueryDict(mutable=True)
    key_dict['_filter'] = params
    filter_string = key_dict.urlencode()

    url = reverse(viewname=name, kwargs=kwargs)
    html = """<a href="{}?{}"><button class="btn btn-primary edit-btn">编辑</button></a>""".format(url, filter_string)
    return mark_safe(html)


@register.simple_tag
def delete_privilege(request, name, *args, **kwargs):
    role = request.crc_user.role

    permission_dict = settings.CRC_PERMISSION[role]
    if name not in permission_dict:
        return ""

    modal_id = kwargs.get('modal_id')
    html = """<button class="btn btn-danger delete-btn" data-bs-toggle="modal" data-bs-target="#{}">删除
            </button>""".format(modal_id)
    return mark_safe(html)
