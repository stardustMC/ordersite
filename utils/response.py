import json

from django.http import JsonResponse


class BaseResponse:

    def __init__(self, status: bool, details):
        self.status = status
        if isinstance(details, str):
            self.details = details
        elif isinstance(details, dict):
            self.details = json.dumps(details)

    def as_json(self):
        return JsonResponse({
            "status": self.status,
            "details": self.details,
        })
