from typing import List
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.db.models import QuerySet

from .models import Answer, Question, AnswerDistributionMatrix, Distribution, UserSuggestion, UserSuggestionSession
from backend.settings import FEEDBACK_URL

def feedback_index(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('backend/index.html')
    return HttpResponse(template.render({
        "foo": "bar"
    }, request))

def create_mapping(request: HttpRequest, hit_types: List, answers: QuerySet[Answer], session: UserSuggestionSession)  -> AnswerDistributionMatrix:
    """
    Creates a suggestion mapping from the given POST data
    """
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
    new_mapping.session = session
    new_mapping.save()
    return new_mapping

def suggest_mapping_removal(request: HttpRequest, matrix: QuerySet[AnswerDistributionMatrix], session: UserSuggestionSession) -> AnswerDistributionMatrix:
    """
    Suggest removal of a mapping

    Returns:
        Either the deletion suggestion mapping in case the original mapping is not a suggestion OR
        The original mapping in case the original mapping is a suggestion
    """
    mapping = matrix.get(id=request.GET.get("mapping")) 
    matches =  matrix.filter(description=mapping.description, isSuggestion=True, isNegativeSuggestion=True)
    is_present = matches.count() > 0
    if not is_present:
        mapping.pk = None
        mapping.isSuggestion = True
        mapping.isNegativeSuggestion = True
        mapping.session = session
        mapping.save()
        return mapping
    else:
        got = matches.first()
        original_mapping = matrix.filter(description=mapping.description, isNegativeSuggestion=False).first()
        got.delete()
        return original_mapping
    return None

def suggest_distro_move(request: HttpRequest, distros: QuerySet[Distribution], matrix: QuerySet[AnswerDistributionMatrix], session: UserSuggestionSession):

    distro = distros.get(id=request.GET.get("distro"))
    mapping_id = request.GET.get("old_mapping")
    old_mapping = None
    mapping = None
    if mapping_id:
        old_mapping = matrix.get(id=request.GET.get("old_mapping"))
    new_mapping_id = request.GET.get("mapping")
    if new_mapping_id:
        mapping = matrix.get(id=request.GET.get("mapping")) 

    if UserSuggestion.objects.filter(distro=distro, new_mapping=mapping).count() == 0 and mapping.distros.filter(id=distro.id).count() == 0:
        suggestion = UserSuggestion(
            distro = distro,
            old_mapping = old_mapping,
            new_mapping = mapping,
            session = session
        )
        suggestion.save()
        return suggestion
    return None

def feedback_selection_reasons(request: HttpRequest, token: str = None) -> HttpResponse:
    if not token:
        session = UserSuggestionSession()
        session.save()
        return HttpResponseRedirect(f"/matrix/{session.sessionToken}")

    readonly_match = UserSuggestionSession.objects.filter(readonlyToken=token)
    session = None
    is_readonly = False
    if readonly_match.count() == 1:
        session = readonly_match.get()
        is_readonly = True
    else:
        session = UserSuggestionSession.objects.get(sessionToken=token)

    template = loader.get_template('backend/selection_reasons.html')
    questions = Question.objects.all()
    answers = Answer.objects.all()

    hit_types = ["isBlockingHit", "isNeutralHit", "isNegativeHit", "isTagOnlyHit"]#

    return_url = None

    if request.method == "POST" and "action" in request.POST:
        action = request.POST.get("action")
        if action == "create":
            got = create_mapping(request, hit_types, answers, session)
            if got:
                return_url = f"returnto={got.answer.id}&returnmapping={got.id}&returnquestion={got.answer.question.id}"
    
    matrix = AnswerDistributionMatrix.objects.all()
    is_moving =  request.GET.get("action") and  request.GET.get("action") == "move"
    is_creating_mapping = request.GET.get("action") and  request.GET.get("action") == "create"
    is_deleting = request.GET.get("action") and  request.GET.get("action") == "delete"

    distros = Distribution.objects.all().order_by("name")
    other_mappings = None
    old_mapping = None
    mapping = None
    old_answer = None
    distro = None
    action =  request.GET.get("action")
    # Allow the user to escape the session and start a new one
    if is_readonly and (action is not None or request.method == "POST"): 
        session = UserSuggestionSession()
        session.save()
        is_readonly = False

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
                obj = UserSuggestion.objects.filter(distro=distro).filter(new_mapping=old_mapping).get()
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
                        is_removal=True,
                        session=session
                    )
                    delete_suggestion.save()
            return_url = f"returnto={old_mapping.answer.id}&returnmapping={old_mapping.id}&returnquestion={old_mapping.answer.question.id}"
        else:
            got = suggest_distro_move(request, distros, matrix, session)
            if got:
                return_url = f"returnto={got.new_mapping.answer.id}&returnmapping={got.id}&returnquestion={got.new_mapping.answer.question.id}"

    if is_deleting:
        got = suggest_mapping_removal(request, matrix, session)
        if got:
            return_url = f"returnto={got.answer.id}&returnmapping={got.id}&returnquestion={got.answer.question.id}"
    if is_creating_mapping:
        answer_id = request.GET.get("answer")
        old_answer = Answer.objects.get(id=answer_id)

    
    if return_url:
        return HttpResponseRedirect(f"/matrix/{session.sessionToken}?{return_url}")
    
    new_mapping_suggestions = AnswerDistributionMatrix.objects.filter(isSuggestion=True, session=session)
    suggested_items = UserSuggestion.objects.filter(session=session)
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
        "language_code": "en",
        "session": session,
        "feedback_url": f"{FEEDBACK_URL}matrix/{session.sessionToken}",
        "readonly_url": f"{FEEDBACK_URL}matrix/{session.readonlyToken}",
        "is_readonly": is_readonly
    }, request))