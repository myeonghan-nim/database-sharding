import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import UserActivity


@method_decorator(csrf_exempt, name="dispatch")
class UserActivityView(View):
    def get(self, request, user_id=None):
        if user_id:
            activities = UserActivity.objects.filter(user_id=user_id)
        else:
            activities = UserActivity.objects.all()
        data = [{"id": activity.id, "user_id": activity.user_id, "action": activity.action} for activity in activities]
        return JsonResponse({"activities": data})

    def list(self, request):
        activities = UserActivity.objects.all()
        data = [{"id": activity.id, "user_id": activity.user_id, "action": activity.action} for activity in activities]
        return JsonResponse({"activities": data})

    def post(self, request):
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        activity = UserActivity.objects.create(user_id=user_id, action=action)
        return JsonResponse({"id": activity.id, "user_id": activity.user_id, "action": activity.action})

    def put(self, request, user_id, pk):
        activities = UserActivity.objects.filter(id=pk, user_id=user_id)
        if not activities.exists():
            return JsonResponse({"message": "Activity not found"}, status=404)
        else:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"message": "Invalid JSON"}, status=400)

            activity = activities.first()
            action = data.get("action")
            activity.action = action
            activity.save()
            return JsonResponse({"id": activity.id, "user_id": activity.user_id, "action": activity.action})

    def delete(self, request, user_id, pk):
        activities = UserActivity.objects.filter(id=pk, user_id=user_id)
        if not activities.exists():
            return JsonResponse({"message": "Activity not found"}, status=404)
        else:
            activity = activities.first()
            activity.delete()
            return JsonResponse({"message": "Deleted successfully"})
