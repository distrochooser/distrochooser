from django.db import models
from backend.settings import MEDIA_ROOT
from django.utils.timezone import now
from distrochooser.constants import COMMIT
from taggit.managers import TaggableManager

class Translateable(models.Model):
    msgid = models.CharField(
        max_length=100, default="new-value", blank=False, null=False)

    class Meta():
        indexes = [
            models.Index(fields=['msgid'])
        ]
        abstract = True


class Category(Translateable):
    index = models.IntegerField(default=0)
    iconClass = models.TextField(default="far fa-circle")

    def __str__(self):
        return "{0}: {1}".format(self.index, self.msgid)


class Question(Translateable):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)
    additionalInfo = models.CharField(
        max_length=200, null=True, blank=True, default=None)
    isMultipleChoice = models.BooleanField(default=False)
    # question with images instead of answers
    isMediaQuestion = models.BooleanField(default=False)

    def __str__(self):
        return self.msgid


class Answer(Translateable):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    blockedAnswers = models.ManyToManyField(
        to="Answer", related_name="blockedAnswersFromAnswer", blank=True)
    mediaSourcePath = models.TextField(
        null=True, blank=True)  # if null -> no image there!
    isDisabled = models.BooleanField(default=False)
    orderIndex = models.IntegerField(default=0)
    tag_prexfix = models.CharField(default=None,blank=True,null=True, max_length=25)
    tags = TaggableManager(blank=True)
    def __str__(self):
        return "{0}: {1}".format(self.question, self.msgid)


class UserSession(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['publicUrl']),
        ]
    dateTime = models.DateTimeField(default=now)
    userAgent = models.CharField(
        max_length=200, null=False, blank=False, default="")
    # is used that only the initial user can edit feedback
    sessionToken = models.CharField(
        max_length=200, null=False, blank=False, default="")
    token = models.CharField(
        max_length=200, null=False, blank=False, default="")
    publicUrl = models.CharField(
        max_length=200, null=False, blank=False, default="")
    language = models.CharField(
        max_length=10, null=False, blank=False, default="en")
    remarks = models.CharField(
        max_length=3000, null=True, blank=True, default=None)
    referrer = models.URLField(
        null=True, blank=True, default=None, max_length=1000)
    calculationTime = models.IntegerField(default=0)
    commit = models.CharField(
        max_length=200, null=True, blank=True, default="")
    calculationEndTime = models.DateTimeField(
        null=True, blank=True, default=None)
    remarksProcessed = models.BooleanField(default=False)
    hardware_cores = models.IntegerField(default=-1)
    hardware_frequency = models.IntegerField(default=-1)
    hardware_memory = models.IntegerField(default=-1)
    hardware_storage = models.IntegerField(default=-1)
    hardware_is_touch = models.BooleanField(default=False)
    filter_by_hardware = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1}".format(self.dateTime, self.publicUrl)

    def save(self, *args, **kwargs):
        self.publicUrl = self.token
        self.commit = COMMIT
        super(UserSession, self).save(*args, **kwargs)

class GivenAnswer(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['answer'])
        ]
    session = models.ForeignKey(
        UserSession, on_delete=models.CASCADE, db_index=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
    isImportant = models.BooleanField(default=False)
    isLessImportant = models.BooleanField(default=False)
    tags = TaggableManager()

    def __str__(self):
        return "{0}: {1}".format(self.session, self.answer)


class Distribution(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['identifier']),
        ]
    name = models.CharField(max_length=200, null=True, blank=True, default="")
    identifier = models.CharField(
        max_length=200, null=True, blank=True, default="")
    fgColor = models.CharField(
        max_length=200, null=True, blank=True, default="")
    bgColor = models.CharField(
        max_length=200, null=True, blank=True, default="")
    logo = models.FileField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    ratings = models.IntegerField(default=0)
    positive_ratings = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    rank = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    hardware_requirements_present = models.BooleanField(default=False)
    hardware_cores = models.IntegerField(default=-1)
    hardware_frequency = models.IntegerField(default=-1)
    hardware_memory = models.IntegerField(default=-1)
    hardware_storage = models.IntegerField(default=-1)
    hardware_has_touch_support = models.BooleanField(default=False)
    data_id = models.CharField(max_length=10, default=None,blank=True,null=True)
    version = models.CharField(max_length=10, default=None,blank=True,null=True)
    founded = models.CharField(max_length=10, default=None,blank=True,null=True)
    age = models.IntegerField(default=None,null=True,blank=True)

    def __str__(self):
        return self.name


class ResultDistroSelection(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['session']),
        ]
    distro = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, default=None)
    session = models.ForeignKey(
        UserSession, on_delete=models.CASCADE, default=None, db_index=True)
    isApprovedByUser = models.BooleanField(default=False)
    isDisApprovedByUser = models.BooleanField(default=False)

    def __str__(self):
        return "{0:} {1}".format(self.session, self.distro)


class SelectionReason(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['resultSelection']),
        ]
    resultSelection = models.ForeignKey(
        ResultDistroSelection, on_delete=models.CASCADE, default=None)
    description = models.CharField(default='', max_length=300, blank=False)
    isPositiveHit = models.BooleanField(default=True)
    isBlockingHit = models.BooleanField(default=False)  # "No-go"
    isRelatedBlocked = models.BooleanField(default=False)
    # e. g. "professional user" for ubuntu ->
    isNeutralHit = models.BooleanField(default=False)
    # if answer was flagged as important
    isImportant = models.BooleanField(default=False)
    isLessImportant = models.BooleanField(default=False)

    def __str__(self):
        return "{0}: P{1}-B{2}-RB{3}-N{4}-I{5}".format(self.description, self.isPositiveHit, self.isBlockingHit, self.isRelatedBlocked, self.isNeutralHit, self.isImportant)


class AnswerDistributionMatrix(models.Model):
    class Meta():
        indexes = [
            models.Index(fields=['answer'])
        ]
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
    isBlockingHit = models.BooleanField(default=False)
    isNegativeHit = models.BooleanField(default=False)
    # e. g. "professional user" for ubuntu ->
    isNeutralHit = models.BooleanField(default=False)

    # only used to allow tag mapping
    isTagOnlyHit = models.BooleanField(default=False)
    description = models.CharField(default='', max_length=300, blank=False)
    distros = models.ManyToManyField(
        to=Distribution, related_name="answerMatrixDistros", blank=True)

    def __str__(self):
        return "Blocking: {0}, Negative: {1}, Neutral: {2}, {3} ({4})".format(self.isBlockingHit, self.isNegativeHit, self.isNeutralHit, self.answer, self.distros.all().values_list("name", flat=True))
