from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name