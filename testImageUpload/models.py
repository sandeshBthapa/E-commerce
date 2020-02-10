from django.db import models


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    # impDoc = models.FileField() # for file upload.

    def __str__(self):
        return self.title
