from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

white_list = [
    '/seller/login/',
    '/seller/register/',
    '/'  # 放行首页
]


class AccessControl(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if '/buyer/' in path:
            return None
        if path in white_list:
            return None

        seller_id = request.COOKIES.get("seller_id")
        if seller_id:
            return None
        return redirect('/seller/login/')
