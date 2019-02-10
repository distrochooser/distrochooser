from django.contrib import admin
from .models import Question, Answer, GivenAnswer, UserSession, ResultDistroSelection, Distribution, SelectionReason, Category

[admin.site.register(*models) for models in [
  (Question,),
  (Answer,),
  (GivenAnswer,),
  (UserSession,),
  (ResultDistroSelection,),
  (Distribution,),
  (SelectionReason,),
  (Category,),
]]