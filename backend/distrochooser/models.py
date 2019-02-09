from django.db import models

class Translateable(models.Model):
  msgid = models.CharField(max_length=100, default="new-value",blank=False, null=False)
  class Meta:
    abstract = True

class Question(Translateable):
  def __str__(self):
    return self.msgid


class Answer(Translateable):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  def __str__(self):
    return "{0}: {1}".format(self.question, self.msgid)

class Result(models.Model):
  pass


class GivenAnswer(models.Model):
  result = models.ForeignKey(Result, on_delete=models.CASCADE)
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
  isImportant = models.BooleanField(default=False)

class Distribution(models.Model):
  pass

class SelectionReason(models.Model):
  pass

class ResultDistroSelection(models.Model):
  distro = models.ForeignKey(Distribution, on_delete=models.CASCADE)
  reason = models.ForeignKey(SelectionReason, on_delete=models.CASCADE)
  result = models.ForeignKey(Result, on_delete=models.CASCADE)