from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    joindate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User({self.name}, {self.email}, {self.gender}, {self.joindate})'