from django.db import models


class TribalUser(models.Model):
    email=models.CharField(max_length=80)
    type_user=models.CharField(max_length=60)
    mobile=models.IntegerField()
    category=models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Organisation(models.Model):
    email=models.CharField(max_length=50, default=' ')
    desc=models.CharField(max_length=600,default=' ')
    mobile=models.IntegerField(max_length=10)
    org_name=models.CharField(max_length=100, default=' ')

    def __str__(self):
        return self.email

class TribalSkills(models.Model):
    img = models.ImageField(upload_to='pics/', default=" ")
    title=models.CharField(max_length=80, default=" ")
    desc=models.CharField(max_length=200, default=" ")
    email=models.CharField(max_length=80, default=" ")

    def __str__(self):
        return self.title

class Apply_tribal_to_org(models.Model):
    tribalemail=models.CharField(max_length=80,default='')
    orgemail=models.CharField(max_length=80,default='')
    application=models.CharField(max_length=1000,default='')
    status=models.CharField(max_length=80,default='')    
    
    def __str__(self):
        return self.tribalemail

class Invite_tribal_to_org(models.Model):
    tribalemail=models.CharField(max_length=80,default='')
    orgemail=models.CharField(max_length=80,default='')
    application=models.CharField(max_length=1000,default='')
    status=models.CharField(max_length=80,default='')

    def __str__(self):
        return self.tribalemail
    