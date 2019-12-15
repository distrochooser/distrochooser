from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict

def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  allAnswers =  Answer.objects.all()
  for answer in rawAnswers:
    givenAnswer = GivenAnswer()
    givenAnswer.session = userSession
    givenAnswer.answer = allAnswers.get(msgid=answer['msgid'])
    givenAnswer.isImportant = answer['important']
    givenAnswer.save()

from django.db import connection
from silk.profiling.profiler import silk_profile
@silk_profile()
def getSelections(userSession, data, langCode):
  translationToUse = TRANSLATIONS[langCode] if langCode in TRANSLATIONS else TRANSLATIONS["en"]
  ResultDistroSelection.objects.filter(session=userSession).delete()
  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession).prefetch_related('answer').values("answer","isImportant")
  importantAnswers = list(map(lambda o: o["answer"], filter(lambda o: o["isImportant"], givenAnswers)))
  distros = Distribution.objects.all()
  matchingTuples = AnswerDistributionMatrix.objects.all().prefetch_related('distros', 'answer')
  distroReasons = {}
  createdSelections = {}
  reasonsBySelection = {}

  for distro in distros:
    selection = ResultDistroSelection()
    selection.session = userSession
    selection.distro = distro
    selection.save()
    createdSelections[distro.id] = selection
    reasonsBySelection[selection.id] = []
  
  for matrixTuple in matchingTuples:
    if matrixTuple.answer not in (o["answer"] for o in givenAnswers):
      pass
    selectedDescription = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description 


    reason = SelectionReason()
    reason.isImportant = matrixTuple.answer.pk in importantAnswers
    reason.resultSelection = None

    reason.isBlockingHit = matrixTuple.isBlockingHit
    reason.isPositiveHit = not matrixTuple.isNegativeHit
    reason.isNeutralHit = matrixTuple.isNeutralHit
    reason.description = selectedDescription

    if reason.isNeutralHit:
      reason.isPositiveHit = True
      
    for distro in matrixTuple.distros.all():
      selection = createdSelections[distro.id]
      # prevent that same descritptions appear multiple times
      isDescriptionAlreadyInReasonList = len(list(filter(lambda r: r.description == reason.description,reasonsBySelection[selection.id]))) > 0
      if not isDescriptionAlreadyInReasonList:
        reason.resultSelection = selection
        reasonsBySelection[selection.id].append(reason)

  results = []
  for _, selection in createdSelections.items():
    reasons = reasonsBySelection[selection.id]
    SelectionReason.objects.bulk_create(reasons)
    results.append(
      {
        "distro": model_to_dict(selection.distro, exclude=["logo", "id"]),
        "reasons": list(map(lambda r: model_to_dict(r,exclude=["id", "resultSelection"]), reasons)),
        "selection": selection.id
      }
    )
  return results