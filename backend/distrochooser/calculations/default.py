from distrochooser.constants import TRANSLATIONS
from distrochooser.models import  GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db import transaction
from django.db.models import Q
from typing import Tuple

def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  newAnswers = []
  selectedAnswers = {answer[0]: answer[1] for answer in Answer.objects.filter(msgid__in=[a["msgid"] for a in rawAnswers]).values_list('msgid', 'pk')}
  for answer in rawAnswers:
    newAnswers.append(
      GivenAnswer(
          session=userSession,
          answer_id=selectedAnswers[answer['msgid']],
          isImportant=answer['important']
      )
    )
  received = GivenAnswer.objects.bulk_create(newAnswers)
  answer: GivenAnswer
  for answer in received:
    raw_objs = list(filter(lambda a: a["msgid"] == answer.answer.msgid, rawAnswers))
    if len(raw_objs) == 1:
      if "tags" in raw_objs[0]:
        tags = raw_objs[0]["tags"]
        for tag in tags:
          answer.tags.add(tag)
      answer.save()

def get_statistics(distro_id: int) -> Tuple[float, int, int]:
  """
  Returns the percentage of approval for the given distro

  Returns:
    A tuple of the percentage, the amount of positive votes and the overall vote count.
    Meaning of the first value:
    positive float: More users approve this selections
    negative float: More user disapprove this result
    50: Equal count of approvals/ disapprovals
    0: No ratings yet
  """
  
  # Get all voted results for this distribution
  selections = ResultDistroSelection.objects.filter(distro=distro_id).filter(Q(isApprovedByUser=True) | Q(isDisApprovedByUser=True))

  approved_by_user= selections.filter(isApprovedByUser=True).count()
  all_count = selections.count()
  not_approved_by_user = all_count - approved_by_user
  percentage = 0
  if approved_by_user > 0:
    percentage = (100/(all_count/ approved_by_user)) if approved_by_user != 0 else 0
  elif not_approved_by_user == approved_by_user and approved_by_user == 0:
    percentage = 0
  elif not_approved_by_user == approved_by_user:
    percentage = 50
  else:
    percentage = -1 * (100/(all_count/ not_approved_by_user)) if not_approved_by_user != 0 else 0

  return round(percentage,0), approved_by_user, all_count

@transaction.atomic
def getSelections(userSession, data, langCode):
  translationToUse = TRANSLATIONS[langCode] if langCode in TRANSLATIONS else TRANSLATIONS["en"]
  ResultDistroSelection.objects.filter(session=userSession).delete()
  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession).prefetch_related('answer').values("answer","isImportant")
  importantAnswers = list(map(lambda o: o["answer"], filter(lambda o: o["isImportant"], givenAnswers)))
  distros = Distribution.objects.all()
  matchingTuples = AnswerDistributionMatrix.objects.all().prefetch_related('distros', 'answer')


  createdSelections = {}
  createdReasons = {}


  newSelections = []
  matchedTags = {}
  for distro in distros:
    selection = ResultDistroSelection(
      session=userSession,
      distro=distro
    )
    newSelections.append(selection)
    createdSelections[distro.id] = selection
    createdReasons[distro.id] = []
    selection.save()

  for matrixTuple in matchingTuples:
    isInAnswerList = matrixTuple.answer.pk in (o["answer"] for o in givenAnswers)
    if isInAnswerList:
      matchedGivenAnswer = GivenAnswer.objects.filter(session=userSession, answer=matrixTuple.answer).first()
      selectedDescription = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description

      reason = SelectionReason(
        isImportant = matrixTuple.answer.pk in importantAnswers,
        resultSelection = None,
        isBlockingHit = matrixTuple.isBlockingHit,
        isPositiveHit = not matrixTuple.isNegativeHit if not matrixTuple.isNeutralHit else True,
        isNeutralHit = matrixTuple.isNeutralHit,
        description = selectedDescription
      )
      
      # prevent that same descritptions appear multiple times
      isReasonUnique = not len(list(filter(lambda r: r.description == reason.description, createdReasons[distro.id]))) > 0
      
      for distro in matrixTuple.distros.all():
        if isReasonUnique:
          selection = createdSelections[distro.id]
          reason.resultSelection = selection
           # verify peculiarities to match with the distribution
          got = distro.tags.filter(name__in=matchedGivenAnswer.tags.names())
          matchedTags[distro.id] = list(got.values_list("name",flat=True))
          createdReasons[distro.id].append(reason)
          reason.save()
  results = []
  for distroId, selection in createdSelections.items():
    reasons = createdReasons[distroId]
    results.append(
      {
        "distro": model_to_dict(selection.distro, exclude=["logo", "id", "tags"]),
        "reasons": list(map(lambda r: model_to_dict(r,exclude=["id", "isDisApprovedByUser"]), reasons)),
        "selection": selection.id,
        "tags": matchedTags[distroId] if distroId in matchedTags else [],
        "percentage": selection.distro.percentage,
        "positive_ratings": selection.distro.positive_ratings,
        "ratings": selection.distro.ratings,
        "rank": selection.distro.rank
      }
    )
  return results