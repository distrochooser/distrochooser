from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from distrochooser.models import UserSession, Question, Distribution, Category, Answer, ResultDistroSelection, SelectionReason, GivenAnswer
import secrets
from distrochooser.constants import TRANSLATIONS
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

def goToStep(categoryIndex: int) -> dict:
  results = Question.objects.filter(category__index=categoryIndex)
  if results.count() == 0:
    raise Exception("Question unknown")
  question = results.first()
  answers = Answer.objects.filter(question=question)
  return {
    "question": model_to_dict(question, fields=('id', 'msgid', 'isMultipleChoice')),
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
  session.token = secrets.token_hex(5) # generate a random token for the user
  session.save()


  questionAndCategoryData = goToStep(0)
  return getJSONCORSResponse({
    "token": session.token,
    "translation": TRANSLATIONS["de-de"],
    "question": questionAndCategoryData["question"],
    "category": questionAndCategoryData["category"],
    "categories": list(Category.objects.all().values()),
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
  #TODO: Store answers
  """
  class GivenAnswer(models.Model):
  session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
  isImportant = models.BooleanField(default=False)
  """
  data = loads(request.body)

  for answer in data['answers']:
    givenAnswer = GivenAnswer()
    givenAnswer.session = userSession
    givenAnswer.answer = Answer.objects.get(msgid=answer['msgid'])
    givenAnswer.isImportant = False
    givenAnswer.save()


  #TODO: Add decision process here
  
  #TODO: After the decision: Add session to distribution map (e. g. session XY -> Debian, XY -> Ubuntu) -> ResultDistroSelection
  userSession = UserSession.objects.first()

  selection = ResultDistroSelection()
  selection.distro = Distribution.objects.first()
  selection.session = userSession #todo: userfeedback
  selection.save()

  #TODO: Add the reasons why Distribution XY was selected -> SelectionReason
  reason = SelectionReason()
  reason.resultSelection = selection
  reason.description = "Because this is a test tuple"
  reason.save()
  reason2 = SelectionReason()

  reason2.resultSelection = selection
  reason2.description = "Because this is a test tuple"
  reason2.isBlockingHit = True
  reason2.save()

  reason3 = SelectionReason()
  reason3.resultSelection = selection
  reason3.description = "Because this is a test tuple"
  reason3.isBlockingHit = False
  reason3.isPositiveHit = False
  reason3.save()

  # Build Result Data

  selections = [
    {
      "distro": model_to_dict(selection.distro),
      "reasons": [
        model_to_dict(reason,fields=["description","isPositiveHit", "isBlockingHit"]),
        model_to_dict(reason2,fields=["description","isPositiveHit", "isBlockingHit"]),
        model_to_dict(reason3,fields=["description","isPositiveHit", "isBlockingHit"])
      ]
    },
    {
      "distro": model_to_dict(selection.distro),
      "reasons": [
        model_to_dict(reason,fields=["description","isPositiveHit", "isBlockingHit"]),
        model_to_dict(reason2,fields=["description","isPositiveHit", "isBlockingHit"]),
        model_to_dict(reason3,fields=["description","isPositiveHit", "isBlockingHit"])
      ]
    }
  ]

  return getJSONCORSResponse({
    "url": "https://distrochooser.de/somecrypticshit",
    "selections": selections
  })