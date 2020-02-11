from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db import transaction

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
  GivenAnswer.objects.bulk_create(newAnswers)


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
  for distro in distros:
    selection = ResultDistroSelection()
    selection.session = userSession
    selection.distro = distro
    newSelections.append(selection)
    createdSelections[distro.id] = selection
    createdReasons[distro.id] = []
    selection.save()


  for matrixTuple in matchingTuples:
    isInAnswerList = matrixTuple.answer.pk in (o["answer"] for o in givenAnswers)
    if isInAnswerList:
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
        selection = list(filter(lambda s: s.distro == distro, newSelections))[0]
        # prevent that same descritptions appear multiple times
        
        isDescriptionAlreadyInReasonList = len(list(filter(lambda r: r.description == reason.description, createdReasons[distro.id]))) > 0
        if not isDescriptionAlreadyInReasonList:
          reason.resultSelection = selection
          createdReasons[distro.id].append(reason)
          reason.save()

  results = []
  for distroId, selection in createdSelections.items():
    reasons = createdReasons[distroId]
    results.append(
      {
        "distro": model_to_dict(selection.distro, exclude=["logo", "id"]),
        "reasons": list(map(lambda r: model_to_dict(r,exclude=["id", "resultSelection"]), reasons)),
        "selection": selection.id
      }
    )
  return results
