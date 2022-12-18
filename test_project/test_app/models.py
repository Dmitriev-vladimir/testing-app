from django.contrib.auth.models import User
from django.db import models


class TestCase(models.Model):
    title = models.CharField(max_length=200)
    temp_correct = models.IntegerField(default=0)
    temp_wrong = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Test(models.Model):
    question = models.CharField(max_length=500)
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=300)
    is_right = models.BooleanField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
