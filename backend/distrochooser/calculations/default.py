from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db import transaction

from threading import Thread, current_thread

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
def saveSelections(selections, reasons, session):
  #  Saves the selections and reasons for a session
  # cleanup old infos -> have no relevance, only the _final_ result is wanted
  ResultDistroSelection.objects.filter(session=session).delete()
  for distro_id, selection in selections.items():
    got = selection.save()
    key = selection.pk
    if key is None:
      raise Exception("Invalid selection id for ", selection.session, "distro", distro_id)
    reasons_list = reasons[distro_id]
    for reason in reasons_list:
      reason.resultSelection = ResultDistroSelection.objects.get(pk=key)
      reason.save()
  

@transaction.atomic
def getSelections(userSession, data, langCode):
  translationToUse = TRANSLATIONS[langCode] if langCode in TRANSLATIONS else TRANSLATIONS["en"]
  ResultDistroSelection.objects.filter(session=userSession).delete()
  saveAnswers(userSession, data['answers'])

  givenAnswers = GivenAnswer.objects.filter(session=userSession).prefetch_related('answer').values("answer","isImportant")
  importantAnswersIds = list(map(lambda o: o["answer"], filter(lambda o: o["isImportant"], givenAnswers)))
  givenAnswerIds = list(map(lambda o: o["answer"], givenAnswers))
  distros = Distribution.objects.all()
  matchingTuples = AnswerDistributionMatrix.objects.filter(answer_id__in=givenAnswerIds).prefetch_related('distros', 'answer')

  createdSelections = {}
  createdReasons = {}


  newSelections = []
  for distro in distros:
    selection = ResultDistroSelection(
      session=userSession,
      distro=distro
    )
    newSelections.append(selection)
    createdSelections[distro.id] = selection
    createdReasons[distro.id] = []
    #selection.save()

  for matrixTuple in matchingTuples:
    selectedDescription = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description

    reason = SelectionReason(
      isImportant = matrixTuple.answer.pk in importantAnswersIds,
      resultSelection = None,
      isBlockingHit = matrixTuple.isBlockingHit,
      isPositiveHit = not matrixTuple.isNegativeHit if not matrixTuple.isNeutralHit else True,
      isNeutralHit = matrixTuple.isNeutralHit,
      description = selectedDescription
    )
    for distro in matrixTuple.distros.all():
      # prevent that same descritptions appear multiple times
      isReasonUnique = not len(list(filter(lambda r: r.description == reason.description, createdReasons[distro.id]))) > 0
      if isReasonUnique:
        selection = createdSelections[distro.id]
        reason.resultSelection = selection
        createdReasons[distro.id].append(reason)
        #reason.save()

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
  # Selections and reasons have no usage in the frontend itself.
  # It's meant to be used for later usage
  t = Thread(target=saveSelections, args=[createdSelections, createdReasons, userSession], daemon=True)
  t.start()
  return results