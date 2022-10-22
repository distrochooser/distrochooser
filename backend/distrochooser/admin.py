from django.contrib import admin
from .models import GivenPeculiarities, Question, Answer, GivenAnswer, GivenPeculiarities, UserSession, ResultDistroSelection, Distribution, SelectionReason, Category, AnswerDistributionMatrix

[admin.site.register(*models) for models in [
  (Question,),
  (GivenAnswer,),
  (GivenPeculiarities,),
  (UserSession,),
  (ResultDistroSelection,),
  (Distribution,),
  (SelectionReason,),
]]

class CategoryAdmin(admin.ModelAdmin):
  def get_ordering(self, request):
     return ['index']
admin.site.register(Category, CategoryAdmin)

class AnswerAdmin(admin.ModelAdmin):
  def get_ordering(self, request):
     return ['question']
admin.site.register(Answer, AnswerAdmin)

class AnswerDistributionMatrixAdmin(admin.ModelAdmin):
  def get_ordering(self, request):
     return ['answer__question']
admin.site.register(AnswerDistributionMatrix, AnswerDistributionMatrixAdmin)