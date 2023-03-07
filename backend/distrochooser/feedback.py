from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Answer, Question, AnswerDistributionMatrix

def feedback_index(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('backend/index.html')
    return HttpResponse(template.render({
        "foo": "bar"
    }, request))

def feedback_selection_reasons(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('backend/selection_reasons.html')
    questions = Question.objects.all()
    answers = Answer.objects.all()

    matrix = AnswerDistributionMatrix.objects.all()
    
    return HttpResponse(template.render({
        "questions": questions,
        "answers": answers,
        "matrix": matrix
    }, request))