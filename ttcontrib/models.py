from django.db import models

# Create your models here.
class Contributor(models.Model):
    c_name = models.CharField(max_length=50)
    c_commits = models.IntegerField()
    c_url = models.URLField(max_length=200)