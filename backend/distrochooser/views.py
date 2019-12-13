from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from distrochooser.models import UserSession, Question, Distribution, Category, Answer, ResultDistroSelection, SelectionReason, GivenAnswer, AnswerDistributionMatrix
import secrets
from distrochooser.constants import TRANSLATIONS, TESTOFFSET
from backend.settings import LOCALES
from django.forms.models import model_to_dict
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt
from distrochooser.calculations import refactored, static
from base64 import b64decode

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

def getStatus(request, slug: str): 
  session = UserSession.objects.filter(token=slug).first()
  if session is None:
    raise Http404

  return JsonResponse({
    "toDo": session.checksToDo,
    "done": session.checksDone
  })

def getLocales(request):
  return getUnsafeJSONCORSResponse(list(LOCALES.keys()))

def getSSRData(request,langCode: str):
  if langCode not in TRANSLATIONS:
    raise Http404
    
  testCount = TESTOFFSET + UserSession.objects.all().count()
  responseData = TRANSLATIONS[langCode].copy()
  responseData["testCount"] = testCount
  return JsonResponse(responseData)

def goToStep(categoryIndex: int) -> dict:
  results = Question.objects.filter(category__index=categoryIndex)
  if results.count() == 0:
    raise Exception("Question unknown")
  question = results.first()
  answers = Answer.objects.filter(question=question)
  responseAnswers = []
  for answer in answers:
    blockedAnswers = []
    for blocked in answer.blockedAnswers.all():
      blockedAnswers.append(blocked.msgid)
    responseAnswers.append({
      "msgid": answer.msgid,
      "blockedAnswers": blockedAnswers
    })
      
  blocking = []
  return {
    "question": model_to_dict(question, fields=('id', 'msgid', 'isMultipleChoice', 'additionalInfo', 'isMediaQuestion')),
    "category": model_to_dict(question.category),
    "answers":  responseAnswers
  }

def start(request: HttpRequest, langCode: str, refLinkEncoded: str):
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
  session.checksToDo = AnswerDistributionMatrix.objects.all().count()
  session.save()
  if refLinkEncoded != "-":
    refLinkDecoded = b64decode(refLinkEncoded).decode("utf-8")
    if refLinkDecoded is not None:
      session.referrer = refLinkDecoded
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

def getLanguage(request, langCode: str):
  if langCode not in LOCALES:
    raise Exception("Language not installed")
  return getJSONCORSResponse({
    "translations": TRANSLATIONS[langCode]
  })

def loadQuestion(request: HttpRequest, langCode: str, index: int, token: str):
  # TODO: Do something with the token
  questionAndCategoryData = goToStep(index)
  return getJSONCORSResponse({
    "question": questionAndCategoryData["question"],
    "answers": questionAndCategoryData["answers"]
  })

@csrf_exempt #TODO: I don't want to disable security features, but the client does not have the CSRF-Cookie?
def submitAnswers(request: HttpRequest, langCode: str, token: str, method: str):
  if langCode not in LOCALES:
    raise Exception("Language not installed")


  userSession = UserSession.objects.get(token=token)
  data = loads(request.body)
  calculations = {
    "static": static.getSelections,
    "refactored": refactored.getSelections
  }
  if method in calculations:
    selections = calculations[method](userSession, data, langCode)
  else:
    raise Exception("Calculation method not known")
  return getJSONCORSResponse({
    "url": "https://beta.distrochooser.de/{0}/{1}/".format(langCode, userSession.publicUrl),
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
  answerList = []
  importanceList = []
  for answer in answers:
    answerList.append(answer.answer.msgid)
    if answer.isImportant:
      importanceList.append(answer.answer.msgid)
  return JsonResponse(
    {
      "answers": answerList,
      "important": importanceList,
      "categories": list(answers.values_list("answer__question__category__msgid",flat=True))
    }
  )