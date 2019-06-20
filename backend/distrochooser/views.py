from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from distrochooser.models import UserSession, Question, Distribution, Category, Answer, ResultDistroSelection, SelectionReason, GivenAnswer, AnswerDistributionMatrix
import secrets
from distrochooser.constants import TRANSLATIONS, TESTOFFSET
from backend.settings import LOCALES
from django.forms.models import model_to_dict
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt

def jumpToQuestion(index: int) -> Question:
  results = Question.objects.filter(category__index=index)
  if results.count() == 0:
    raise Exception("Question unknown")
  return results.get()

def getJSONCORSResponse(data):
  response = JsonResponse(data)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
  return response

def getUnsafeJSONCORSResponse(data):
  response = JsonResponse(data, safe=False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
  return response


def getLocales(request):
  return getUnsafeJSONCORSResponse(list(LOCALES.keys()))

def getTranslation(request,langCode: str):
  if langCode not in TRANSLATIONS:
    raise Http404
  return JsonResponse(TRANSLATIONS[langCode])

def goToStep(categoryIndex: int) -> dict:
  results = Question.objects.filter(category__index=categoryIndex)
  if results.count() == 0:
    raise Exception("Question unknown")
  question = results.first()
  answers = Answer.objects.filter(question=question)
  blocking = []
  return {
    "question": model_to_dict(question, fields=('id', 'msgid', 'isMultipleChoice', 'additionalInfo')),
    "category": model_to_dict(question.category),
    "answers":  list(answers.values("msgid"))
  }

def start(request: HttpRequest, langCode: str):
  """
  'Loggs' the visitor in, creates a session which will be used to store the user's action.
  """
  if langCode not in LOCALES:
    raise Exception("Language not installed")

  userAgent = request.META["HTTP_USER_AGENT"]
  session = UserSession()
  session.userAgent = userAgent
  session.language = langCode
  session.token = secrets.token_hex(5) # generate a random token for the user
  session.save()


  questionAndCategoryData = goToStep(0)
  testCount = TESTOFFSET + UserSession.objects.all().count()
  return getJSONCORSResponse({
    "token": session.token,
    "language": langCode,
    "testCount": testCount,
    "translations": TRANSLATIONS[langCode],
    "question": questionAndCategoryData["question"],
    "category": questionAndCategoryData["category"],
    "categories": list(Category.objects.all().order_by("index").values()),
    "answers": questionAndCategoryData["answers"]
  })

def loadQuestion(request: HttpRequest, langCode: str, index: int, token: str):
  # TODO: Do something with the token
  questionAndCategoryData = goToStep(index)
  return getJSONCORSResponse({
    "question": questionAndCategoryData["question"],
    "answers": questionAndCategoryData["answers"]
  })

@csrf_exempt #TODO: I don't want to disable security features, but the client does not have the CSRF-Cookie?
def submitAnswers(request: HttpRequest, langCode: str, token: str):
  #TODO: Do something with the token

  userSession = UserSession.objects.get(token=token)
  translationToUse = TRANSLATIONS[userSession.language] if userSession.language in TRANSLATIONS else TRANSLATIONS["en"]
  # TODO: Delete old given answers
  GivenAnswer.objects.filter(session=userSession).delete()
  ResultDistroSelection.objects.filter(session=userSession).delete()
  #TODO: Store answers
  data = loads(request.body)
  for answer in data['answers']:
    givenAnswer = GivenAnswer()
    givenAnswer.session = userSession
    givenAnswer.answer = Answer.objects.get(msgid=answer['msgid'])
    givenAnswer.isImportant = False
    givenAnswer.save()

  blockingAnswers = []

  givenAnswers = GivenAnswer.objects.filter(session=userSession)
  distros = Distribution.objects.all()
  selections = []
  for distro in distros:
    # create selection
    # even 0 matches have a selection, with the reason..0 matches
    selection = ResultDistroSelection()
    selection.distro = distro
    selection.session = userSession #todo: userfeedback
    selection.save()
    reasons = []
    answerDistributionMatrixTuples = AnswerDistributionMatrix.objects.filter(distros__in=[distro])
    score = 0
    for matrix in answerDistributionMatrixTuples:
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
        # TODO: CHECK TRANSLATION
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
        if reason.isBlockingHit or reason.isRelatedBlocked:
          score = score - 1
        else:
          if not reason.isNeutralHit:
            score = score + 1
        # prevent that the same reason (got out of different answers) gets counted twice or more
        if len(list(filter(lambda r: r.description ==  reason.description and r.isBlockingHit == reason.isBlockingHit and r.isPositiveHit == reason.isPositiveHit and r.isNeutralHit == reason.isNeutralHit, reasons))) == 1:
          score = score -1 
        else:
          reason.save()
          reasons.append(reason)
    distro = model_to_dict(selection.distro, exclude="logo")
    if selection.distro.logo:
      distro["logo"] = selection.distro.logo.url
    selections.append({
      "distro": distro,
      "reasons": list(map(lambda r: model_to_dict(r), reasons)),
      "score": score,
      "selection": selection.id
    })
 
  return getJSONCORSResponse({
    "url": "https://beta.distrochooser.de/{0}/{1}/".format(userSession.language, userSession.publicUrl),
    "selections": selections,
    "token": token
  })

@csrf_exempt #TODO: I don't want to disable security features, but the client does not have the CSRF-Cookie?
def vote(request): 
  data = loads(request.body)
  id = int(data["selection"])
  got = -1
  if data["positive"] is not None:
    isPositive = data["positive"] == True
    got = ResultDistroSelection.objects.filter(pk=id).update(isApprovedByUser=isPositive,isDisApprovedByUser= not isPositive)
  else:
    got = ResultDistroSelection.objects.filter(pk=id).update(isApprovedByUser=False,isDisApprovedByUser= False)

  return JsonResponse({
    "count": got
  })

@csrf_exempt #TODO: I don't want to disable security features, but the client does not have the CSRF-Cookie?
def updateRemark(request): 
  data = loads(request.body)
  id = data["result"]
  remark = data["remarks"]
  oldSessionObject = UserSession.objects.get(token=id)
  got = -1
  # the remark can be changed once
  # to prevent that it can be overwritten when somebody get's a shared link
  if oldSessionObject.remarks is None:
    got = UserSession.objects.filter(token=id).update(remarks=remark)
  return HttpResponse(got)

def getGivenAnswers(request, slug:str):
  answers = GivenAnswer.objects.filter(session__publicUrl=slug) 
  return JsonResponse(
    {
      "answers": list(answers.values_list("answer__msgid",flat=True)),
      "categories": list(answers.values_list("answer__question__category__msgid",flat=True))
    }
  )