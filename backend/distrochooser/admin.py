from django.contrib import admin
from .models import Question, Answer, GivenAnswer, Result, ResultDistroSelection, Distribution, SelectionReason

[admin.site.register(*models) for models in [
  (Question,),
  (Answer,),
  (GivenAnswer,),
  (Result,),
  (ResultDistroSelection,),
  (Distribution,),
  (SelectionReason,),
]]