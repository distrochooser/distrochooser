from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix
from django.forms.models import model_to_dict
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

def saveReasonsForDistro(distro, givenAnswers, translationToUse, selection): 
  answerDistributionMatrixTuples = AnswerDistributionMatrix.objects.filter(distros__in=[distro])
  return saveReasonForMatrixTuple(selection, answerDistributionMatrixTuples, translationToUse, givenAnswers)

def saveReasonForMatrixTuple(selection, matrixTuples, translationToUse, givenAnswers):
  reasons = []
  for matrix in matrixTuples:
    # check if there is an 1:1 mapping
    if givenAnswers.filter(answer=matrix.answer).count() == 1:

      # check if the selected answer is blocked by another one
      # should prevent answers like beginner + professional in one session
      isRelatedBlocked = False
      description = translationToUse[matrix.answer.question.category.msgid] if matrix.answer.question.category.msgid in translationToUse else matrix.answer.question.category.msgid
      blockedQuestionTexts = []
      for blockedAnswer in matrix.answer.blockedAnswers.all():
        if blockedAnswer.pk in givenAnswers.all().values_list("answer",flat=True):
          isRelatedBlocked = True
          textToAdd = translationToUse[blockedAnswer.question.category.msgid] if blockedAnswer.question.category.msgid in translationToUse else blockedAnswer.question.category.msgid
          if textToAdd not in blockedQuestionTexts:
            blockedQuestionTexts.append( translationToUse[blockedAnswer.question.category.msgid] if blockedAnswer.question.category.msgid in translationToUse else blockedAnswer.question.category.msgid)
    
      reason = SelectionReason()
      reason.resultSelection = selection
      if isRelatedBlocked:
        reason.isBlockingHit = True
        reason.isPositiveHit = False
        reason.isRelatedBlocked = isRelatedBlocked
        reason.description = translationToUse["reason-blocked-by-others-entry"].format(description, "\" and \"".join(blockedQuestionTexts) ) 
      else:
        reason.isBlockingHit = matrix.isBlockingHit
        reason.isPositiveHit = not matrix.isNegativeHit
        reason.isNeutralHit = matrix.isNeutralHit
        if not reason.isNeutralHit:
          reason.description =  translationToUse[matrix.description] if matrix.description in translationToUse else matrix.description 
        else:
          reason.isPositiveHit = True
          reason.description = translationToUse[matrix.description]
      
      # prevent that the same reason (got out of different answers) gets counted twice or more
      if SelectionReason.objects.filter(resultSelection=selection, description=reason.description, isBlockingHit=reason.isBlockingHit, isPositiveHit=reason.isPositiveHit,isNeutralHit=reason.isNeutralHit).count() == 0:
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

  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession)

  distros = Distribution.objects.all()

  distroChunks = list(chunks(distros, 2))
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

      reasons = saveReasonsForDistro(distro, self.givenAnswers, self.translationToUse, selection)
      self.selections.append({
        "distro": model_to_dict(selection.distro, exclude="logo"),
        "reasons": list(map(lambda r: model_to_dict(r), reasons)),
        "selection": selection.id
      })