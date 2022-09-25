from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db import transaction


import plotly.express as px
import pandas as pd

def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  newAnswers = []
  rawSelectedAnswers = Answer.objects.filter(msgid__in=[a["msgid"] for a in rawAnswers]).values_list('msgid', 'pk', 'questionType')
  selectedAnswers = {answer[0]: answer[1] for answer in rawSelectedAnswers}
  for answer in rawAnswers:
    answer_id=selectedAnswers[answer['msgid']]
    newAnswers.append(
      GivenAnswer(
          session=userSession,
          answer_id=answer_id,
          isImportant=answer['important']
      )
    )
  stats = {}
  for answer in rawSelectedAnswers:
    answer_type = answer[2]
    if answer_type is not None:
      if answer_type not in stats:
        stats[answer_type] = 0
      stats[answer_type] = stats[answer_type] + 1
  df = pd.DataFrame(dict(
      r=stats.values(),
      theta=stats.keys()))
  fig = px.line_polar(df, r='r', theta='theta', line_close=True)
  fig.update_layout(polar = dict(radialaxis = dict(showticklabels = False)))
  fig.write_image("foo.png")
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