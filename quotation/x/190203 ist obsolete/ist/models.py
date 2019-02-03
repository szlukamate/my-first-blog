from django.db import models
from django.utils import timezone


class tblIssue(models.Model):
    author_tblIssue = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title_tblIssue = models.CharField(max_length=200)
    text_tblIssue = models.TextField()
    created_tblIssue = models.DateTimeField(
            default=timezone.now)


    def __str__(self):
        return self.title_tblIssue