from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Answer, Question, AnswerDistributionMatrix, Distribution, UserSuggestion

def feedback_index(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('backend/index.html')
    return HttpResponse(template.render({
        "foo": "bar"
    }, request))

def feedback_selection_reasons(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('backend/selection_reasons.html')
    questions = Question.objects.all()
    answers = Answer.objects.all()

    hit_types = ["blocking", "neutral", "negative", "tags"]
    if request.method == "POST" and "action" in request.POST:
        action = request.POST.get("action")
        if action == "create":
            description = request.POST.get("description")
            mapping_spec = {}
            for key in hit_types:
                mapping_spec[key] = request.POST.get(key) == "on"
            new_mapping= AnswerDistributionMatrix()
            new_mapping.description = description
            for key in hit_types:
                new_mapping.__setattr__(key, mapping_spec[key])
            new_mapping.answer = answers.get(id=request.GET.get("answer"))
            new_mapping.isSuggestion = True
            new_mapping.save()
        if action == "delete":
            mapping_id = request.POST.get("mapping")
            raise (mapping_id)
            

    matrix = AnswerDistributionMatrix.objects.all()

    is_moving =  request.GET.get("action") and  request.GET.get("action") == "move"
    is_creating_mapping = request.GET.get("action") and  request.GET.get("action") == "create"
    is_deleting = request.GET.get("action") and  request.GET.get("action") == "delete"

    distros = Distribution.objects.all().order_by("name")
    update_modal_open = is_creating_mapping
    other_mappings = None
    old_mapping = None
    mapping = None
    old_answer = None
    distro = None
    action =  request.GET.get("action")

    if update_modal_open:
        answer_id = request.GET.get("answer")
    if is_moving:
        mapping_id = request.GET.get("old_mapping")
        if mapping_id:
            old_mapping = matrix.get(id=request.GET.get("old_mapping"))
        new_mapping_id = request.GET.get("mapping")
        if new_mapping_id:
            mapping = matrix.get(id=request.GET.get("mapping")) 
        distro = distros.get(id=request.GET.get("distro"))
        if not mapping:
            is_suggestion = old_mapping.isSuggestion
            is_distro_suggestion = request.GET.get("suggestion") is not None
            if is_suggestion: # The suggestion is part of a new mapping suggestion
                obj = UserSuggestion.objects.filter(distro=distro).filter(old_mapping=mapping).get()
                obj.delete()
            elif is_distro_suggestion: # the distro was added/removed to an existing mapping
                suggestion_id = request.GET.get("suggestion")
                UserSuggestion.objects.get(id=suggestion_id).delete()
            else:
                # Add a new suggestion the distro was removed
                if UserSuggestion.objects.filter(distro=distro).filter(old_mapping=old_mapping).filter(is_removal=True).count() == 0:
                    delete_suggestion = UserSuggestion(
                        distro=distro,
                        old_mapping=old_mapping,
                        is_removal=True
                    )
                    delete_suggestion.save()
            print("Would move to bin", distro.name, "from", old_mapping, "to", mapping)
        else:
            print("Would move", distro.name, "from", old_mapping, "to", mapping)
            if UserSuggestion.objects.filter(distro=distro, new_mapping=mapping).count() == 0 and mapping.distros.filter(id=distro.id).count() == 0:
                suggestion = UserSuggestion(
                    distro = distro,
                    old_mapping = old_mapping,
                    new_mapping = mapping
                )
                suggestion.save()

    if is_deleting:
        mapping = matrix.get(id=request.GET.get("mapping")) 
        print("Would delete", mapping)
    if is_creating_mapping:
        answer_id = request.GET.get("answer")
        old_answer = Answer.objects.get(id=answer_id)

    new_mapping_suggestions = AnswerDistributionMatrix.objects.filter(isSuggestion=True)
    suggested_items = UserSuggestion.objects.all()

    return HttpResponse(template.render({
        "action": action,
        "questions": questions,
        "answers": answers,
        "matrix": matrix,
        "hit_types": hit_types,
        "distro": distro,
        "distros": distros,
        "old_answer": old_answer,
        "old_mapping": old_mapping,
        "other_mappings": other_mappings,
        "suggested_items": suggested_items,
        "new_mapping_suggestions": new_mapping_suggestions,
        "language_code": "en"
    }, request))