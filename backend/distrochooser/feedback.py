from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Answer, Question, AnswerDistributionMatrix, Distribution

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

    is_moving =  request.GET.get("action") and  request.GET.get("action") == "move"
    update_modal_open = request.GET.get("distro") is not None and request.GET.get("mapping") is not None
    other_mappings = None
    old_mapping = None
    old_answer = None
    distro = None

    if update_modal_open:
        answer_id = request.GET.get("answer")
        old_mapping = matrix.get(id=request.GET.get("mapping"))
        old_answer = old_mapping.answer
        distro = Distribution.objects.get(id=request.GET.get("distro"))
        other_mappings = AnswerDistributionMatrix.objects.filter(answer_id=answer_id)
    if is_moving:
        old_mapping = matrix.get(id=request.GET.get("old_mapping"))
        mapping = matrix.get(id=request.GET.get("mapping"))
        distro = Distribution.objects.get(id=request.GET.get("distro"))
        print("Would move", distro.name, "from", old_mapping.id, "to", mapping.id)

    return HttpResponse(template.render({
        "questions": questions,
        "answers": answers,
        "matrix": matrix,
        "hit_types": ["blocking", "neutral", "negative", "tags"],
        "distro": distro,
        "old_answer": old_answer,
        "old_mapping": old_mapping,
        "other_mappings": other_mappings
    }, request))