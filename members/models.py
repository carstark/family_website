from django.db import models


class Member(models.Model):
    image = models.ImageField(upload_to='images/')
    full_name = models.CharField(max_length=64)
    abstract = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.full_name
