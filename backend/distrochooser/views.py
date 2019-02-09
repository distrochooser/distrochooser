from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from distrochooser.models import UserSession
import secrets
from distrochooser.constants import TRANSLATIONS
from backend.settings import LOCALES


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
  
  return JsonResponse({
    "token": session.token,
    "translation": TRANSLATIONS["de-de"]
  })