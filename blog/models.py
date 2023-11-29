from django.db import models
from django.contrib.auth.models import User


# Create A blog models
class Blog(models.Model):
    title = models.CharField(max_length=64, help_text="Gibt dem Kind einen Namen!")
    pub_date = models.DateField()
    body = models.TextField()
    image = models.ImageField(upload_to="images/")
    # the upper are added due to portfolio, the below due to product hunter exercise
    url = models.URLField(default="https://nomenetomen.de")
    votes_total = models.PositiveSmallIntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    author_icon = models.ImageField(upload_to="images/", default="vaalser.png")

    def __str__(self):
        return self.title

    def summary(self):
        if len(self.body.split(" ")) < 50:
            # for when the body contains less than 15 words, it returns whatever is there
            return self.body
        else:
            # for when the body is longer than 15 words, it returns just the first 15
            return " ".join(self.body.split(" ")[:50])+"..."


class Vote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
