from django.db import models
from django.conf import settings

# Create your models here.
class Trade(models.Model):
    user_one = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='initiated_trades', on_delete=models.CASCADE)
    user_two = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_trades', on_delete=models.CASCADE)
    skill_given_by_user_one = models.CharField(max_length=100)
    skill_given_by_user_two = models.CharField(max_length=100)
    agreed_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_one.username} ↔ {self.user_two.username}"
