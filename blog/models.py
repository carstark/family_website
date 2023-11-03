from django.db import models

# Create A blog models
class Blog(models.Model):
    title = models.CharField(max_length=64)
    pub_date = models.DateField()
    body = models.TextField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title

    def summary(self):
        if len(self.body.split(" ")) < 15:
            return self.body
        else:
            return " ".join(self.body.split(" ")[:15])+"..."
