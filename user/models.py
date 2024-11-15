from django.db import models


class UserActivity(models.Model):
    user_id = models.IntegerField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_activity"
