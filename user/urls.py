from django.urls import path

from .views import UserActivityView

urlpatterns = [
    path("activity/", UserActivityView.as_view(), name="activity_create"),
    path("activity/<int:user_id>/", UserActivityView.as_view(), name="activity_read"),
    path("activity/<int:user_id>/<int:pk>/", UserActivityView.as_view(), name="activity_update"),
    path("activity/<int:user_id>/<int:pk>/", UserActivityView.as_view(), name="activity_delete"),
]
