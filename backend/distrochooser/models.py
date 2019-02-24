from django.db import models
from datetime import datetime
import string
class Translateable(models.Model):
  msgid = models.CharField(max_length=100, default="new-value",blank=False, null=False)
  class Meta: 
    abstract = True
    

class Category(Translateable):
  index = models.IntegerField(default=0)

class Question(Translateable):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
  isMultipleChoice = models.BooleanField(default=False)
  def __str__(self):
    return self.msgid


class Answer(Translateable):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  def __str__(self):
    return "{0}: {1}".format(self.question, self.msgid)

class UserSession(models.Model):
  dateTime = models.DateTimeField(default=datetime.now())
  userAgent = models.CharField(max_length=200, null=False, blank=False, default="")
  token = models.CharField(max_length=200, null=False, blank=False, default="")
  def __str__(self):
    return "{0} - {1}".format(self.dateTime, self.userAgent)


class GivenAnswer(models.Model):
  session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
  isImportant = models.BooleanField(default=False)

class Distribution(models.Model):
  pass

class ResultDistroSelection(models.Model):
  distro = models.ForeignKey(Distribution, on_delete=models.CASCADE, default=None)
  session = models.ForeignKey(UserSession, on_delete=models.CASCADE, default=None)

class SelectionReason(models.Model):
  resultSelection = models.ForeignKey(ResultDistroSelection, on_delete=models.CASCADE, default=None)
  description = models.CharField(default='', max_length=300, blank=False)
