from django.db import models
from datetime import datetime
import string
from monsterurl import get_monster
class Translateable(models.Model):
  msgid = models.CharField(max_length=100, default="new-value",blank=False, null=False)
  class Meta: 
    abstract = True
    

class Category(Translateable):
  index = models.IntegerField(default=0)
  def __str__(self): 
    return "{0}: {1}".format(self.index, self.msgid)

class Question(Translateable):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
  isMultipleChoice = models.BooleanField(default=False)
  def __str__(self):
    return self.msgid


class Answer(Translateable):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  blockedAnswers =  models.ManyToManyField(to="Answer", related_name="blockedAnswersFromAnswer",blank=True)
  def __str__(self):
    return "{0}: {1}".format(self.question, self.msgid)

class UserSession(models.Model):
  dateTime = models.DateTimeField(default=datetime.now())
  userAgent = models.CharField(max_length=200, null=False, blank=False, default="")
  token = models.CharField(max_length=200, null=False, blank=False, default="")
  publicUrl = models.CharField(max_length=200, null=False, blank=False, default="")
  def __str__(self):
    return "{0} - {1}".format(self.dateTime, self.userAgent)

  def save(self, *args, **kwargs):
    self.publicUrl = get_monster()
    super(UserSession, self).save(*args, **kwargs)

class GivenAnswer(models.Model):
  session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
  isImportant = models.BooleanField(default=False)
  # TODO: IMPORTANCE FLAG
  def __str__(self):
    return "{0}: {1}".format(self.session, self.answer)

class Distribution(models.Model):
  name = models.CharField(max_length=200, null=True, blank=True, default="")
  identifier = models.CharField(max_length=200, null=True, blank=True, default="")
  fgColor = models.CharField(max_length=200, null=True, blank=True, default="")
  bgColor = models.CharField(max_length=200, null=True, blank=True, default="")
  def __str__(self):
    return self.name

class ResultDistroSelection(models.Model):
  distro = models.ForeignKey(Distribution, on_delete=models.CASCADE, default=None)
  session = models.ForeignKey(UserSession, on_delete=models.CASCADE, default=None)
  isApprovedByUser = models.BooleanField(default=False)
  isDisApprovedByUser = models.BooleanField(default=False)

class SelectionReason(models.Model):
  resultSelection = models.ForeignKey(ResultDistroSelection, on_delete=models.CASCADE, default=None)
  description = models.CharField(default='', max_length=300, blank=False)
  isPositiveHit = models.BooleanField(default=True)
  isBlockingHit = models.BooleanField(default=False) # "No-go"
  isRelatedBlocked =  models.BooleanField(default=False)

class AnswerDistributionMatrix(models.Model):
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
  isBlockingHit = models.BooleanField(default=False)
  isNegativeHit = models.BooleanField(default=False)
  description = models.CharField(default='', max_length=300, blank=False)
  distros =  models.ManyToManyField(to=Distribution, related_name="answerMatrixDistros",blank=True)
  def __str__(self):
    return "Blocking: {0}, {1} ({2})".format(self.isBlockingHit, self.answer, self.distros.all().values_list("name",flat=True))