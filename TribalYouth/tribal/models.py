from django.db import models


class TribalUser(models.Model):
    email=models.CharField(max_length=80)
    type_user=models.CharField(max_length=60)
    mobile=models.IntegerField()
    category=models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Organisation(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=25)
    name=models.CharField(max_length=80)
    mobile=models.IntegerField()
    organisation_name=models.CharField(max_length=100)

    def __str__(self):
        return self.email

class TribalSkills(models.Model):
    img = models.ImageField(upload_to='pics/', default=" ")
    title=models.CharField(max_length=80, default=" ")
    desc=models.CharField(max_length=200, default=" ")
    email=models.CharField(max_length=80, default=" ")

    def __str__(self):
        return self.title

