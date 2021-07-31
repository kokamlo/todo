from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=140)
    desc = models.TextField(blank=True)
    createdate = models.DateTimeField(auto_now_add=True)
    compeliteddate = models.DateTimeField(null=True , blank=True)
    checkimportant = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
