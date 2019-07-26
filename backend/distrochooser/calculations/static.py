from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db.models import F
import threading
import time
def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  for answer in rawAnswers:
    givenAnswer = GivenAnswer()
    givenAnswer.session = userSession
    givenAnswer.answer = Answer.objects.get(msgid=answer['msgid'])
    givenAnswer.isImportant = False
    givenAnswer.save()

def saveReasonsForDistro(givenAnswers, translationToUse, selection): 
  answerDistributionMatrixTuples = AnswerDistributionMatrix.objects.filter(distros__pk=selection.distro.pk)
  return saveReasonForMatrixTuple(selection, answerDistributionMatrixTuples, translationToUse, givenAnswers)

def saveReasonForMatrixTuple(selection, matrixTuples, translationToUse, givenAnswers):
  reasons = []

  flatGivenAnswersHaystack = givenAnswers.all().values_list("answer",flat=True)

  for givenAnswer in givenAnswers:
    answer = givenAnswer.answer
    matchingMatrixTuple = matrixTuples.filter(answer=answer)
    description = translationToUse[answer.question.category.msgid] if answer.question.category.msgid in translationToUse else answer.question.category.msgid
    for matrixTuple in matchingMatrixTuple:
      UserSession.objects.filter(pk=selection.session.pk).update(checksDone=F('checksDone') + 1)
      isRelatedBlocked = False
      blockedQuestionTexts = []
      blockedAnswers = matrixTuple.answer.blockedAnswers.filter(pk__in=flatGivenAnswersHaystack)
      isRelatedBlocked = blockedAnswers.count() > 0
      for blockedAnswer in blockedAnswers:
        textToAdd = translationToUse[blockedAnswer.question.category.msgid] if blockedAnswer.question.category.msgid in translationToUse else blockedAnswer.question.category.msgid
        if textToAdd not in blockedQuestionTexts:
          blockedQuestionTexts.append(textToAdd)
      reason = SelectionReason()
      reason.resultSelection = selection
      if isRelatedBlocked:
        reason.isBlockingHit = True
        reason.isPositiveHit = False
        reason.isRelatedBlocked = isRelatedBlocked
        reason.description = translationToUse["reason-blocked-by-others-entry"].format(description, "\" and \"".join(blockedQuestionTexts)) 
      else:
        reason.isBlockingHit = matrixTuple.isBlockingHit
        reason.isPositiveHit = not matrixTuple.isNegativeHit
        reason.isNeutralHit = matrixTuple.isNeutralHit
        reason.description = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description 
        if reason.isNeutralHit:
          reason.isPositiveHit = True
      
      # prevent that the same reason (got out of different answers) gets counted twice or more
      if len(list(filter(lambda r: r.description == reason.description and r.isBlockingHit == reason.isBlockingHit and r.isPositiveHit == reason.isPositiveHit and r.isNeutralHit==reason.isNeutralHit, reasons))) == 0:
        reason.save()
        reasons.append(reason)
  
  return reasons

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

getTime = lambda: int(round(time.time() * 1000))

def getSelections(userSession, data):
  translationToUse = TRANSLATIONS[userSession.language] if userSession.language in TRANSLATIONS else TRANSLATIONS["en"]

  ResultDistroSelection.objects.filter(session=userSession).delete()
  
  UserSession.objects.filter(pk=userSession.pk).update(checksDone=0)
  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession)

  distros = Distribution.objects.all()

  distroChunks = list(chunks(distros, 4))
  threads = []
  for chunk in distroChunks:
    thread = selectingThread(chunk, givenAnswers, translationToUse, userSession)
    threads.append(thread)
  selections = []
  for t in threads:
    t.start()

  for t in threads:
    t.join()
    selections = selections + t.selections
  return selections

class selectingThread (threading.Thread):
  def __init__(self, distributions, givenAnswers, translationToUse, userSession):
    threading.Thread.__init__(self)
    self.distributions = distributions
    self.givenAnswers = givenAnswers
    self.translationToUse = translationToUse
    self.userSession = userSession
    self.selections = []
  def run(self):
    for distro in self.distributions:
      # create selection
      # even 0 matches have a selection, with the reason..0 matches
      selection = ResultDistroSelection()
      selection.distro = distro
      selection.session = self.userSession #todo: userfeedback
      selection.save()
      
      reasons = saveReasonsForDistro(self.givenAnswers, self.translationToUse, selection)
      self.selections.append({
        "distro": model_to_dict(selection.distro, exclude="logo"),
        "reasons": list(map(lambda r: model_to_dict(r), reasons)),
        "selection": selection.id
      })
    