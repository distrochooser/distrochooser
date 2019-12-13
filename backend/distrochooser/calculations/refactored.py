from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict

def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  for answer in rawAnswers:
    givenAnswer = GivenAnswer()
    givenAnswer.session = userSession
    givenAnswer.answer = Answer.objects.get(msgid=answer['msgid'])
    givenAnswer.isImportant = answer['important']
    givenAnswer.save()

def getSelections(userSession, data, langCode):
  translationToUse = TRANSLATIONS[langCode] if langCode in TRANSLATIONS else TRANSLATIONS["en"]
  ResultDistroSelection.objects.filter(session=userSession).delete()
  userSession.checksDone = 0
  userSession.save()
  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession).values("answer","isImportant")
  importantAnswers = list(map(lambda o: o["answer"], filter(lambda o: o["isImportant"], givenAnswers)))
  distros = Distribution.objects.all()
  matrixTuples = AnswerDistributionMatrix.objects.all()
  matchingTuples = matrixTuples.filter(answer_id__in=(o["answer"] for o in givenAnswers))
  distroReasons = {}
  createdSelections = []
  reasonsBySelection = {}

  for distro in distros:
    selection = ResultDistroSelection()
    selection.session = userSession
    selection.distro = distro
    selection.save()
    createdSelections.append(selection)
    reasonsBySelection[selection.id] = []
  
  for matrixTuple in matchingTuples:
    userSession.checksDone = userSession.checksDone +1
    userSession.save()
    reason = SelectionReason()
    reason.isImportant = matrixTuple.answer.pk in importantAnswers
    reason.resultSelection = None

    reason.isBlockingHit = matrixTuple.isBlockingHit
    reason.isPositiveHit = not matrixTuple.isNegativeHit
    reason.isNeutralHit = matrixTuple.isNeutralHit
    reason.description = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description 

    if reason.isNeutralHit:
      reason.isPositiveHit = True
    for distro in matrixTuple.distros.all():
      selection = None
      suitableSelections = list(filter(lambda o: o.distro == distro, createdSelections))
      if len(suitableSelections) != 1:
        raise Exception("Invalid state")
      else:
        selection = suitableSelections[0]
      # prevent that same descritptions appear multiple times
      isDescriptionAlreadyInReasonList = len(list(filter(lambda r: r.description == reason.description,reasonsBySelection[selection.id]))) > 0
      if not isDescriptionAlreadyInReasonList:
        reason.resultSelection = selection
        reason.save()
        reasonsBySelection[selection.id].append(reason)

  results = []
  for selection in createdSelections:
    reasons = reasonsBySelection[selection.id]
    results.append(
      {
        "distro": model_to_dict(selection.distro, exclude="logo"),
        "reasons": list(map(lambda r: model_to_dict(r), reasons)),
        "selection": selection.id
      }
    )
  return results
