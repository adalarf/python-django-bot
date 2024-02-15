from django.views import View
from app.internal.services.user_service import get_user_info
from django.http.response import HttpResponseNotFound, HttpResponse


class GetUserInfoView(View):
    async def get(self, request, id):
        try:
            return HttpResponse(await get_user_info(id))
        except:
            return HttpResponseNotFound("Пользователь не найден")