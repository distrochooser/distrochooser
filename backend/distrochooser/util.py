"""
Generic helper functions to utilize them in several parts of the backend.
"""

from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from distrochooser.models import Question, Answer

from json import loads


def get_json_response(data) -> JsonResponse:
    """
    Returns a HTTP Response with Content-Type application/JSON from the given data parameter

    Args:
      data: The information to json encode

    Returns:
      JsonResponse:The response including needed CORS headers
    """
    response = JsonResponse(data, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


def get_step_data(category_index: int) -> dict:
    """
    Get the question for a given category

    Args:
      category_index (int): The 0-based index of hte category

    Returns:
      dict: A dictionary containing the question, the category and the answers
    """
    results = Question.objects.filter(category__index=category_index)
    if results.count() == 0:
        raise Http404("Question unknown")

    question = results.first()
    answers = Answer.objects.filter(
        question=question, isDisabled=False).order_by("orderIndex")
    response_answers = []
    for answer in answers:
        blocked_answers = []
        for blocked in answer.blockedAnswers.all():
            blocked_answers.append(blocked.msgid)
        tag_slugs = list(answer.tags.slugs())
        tag_translations = {}
        for tag in answer.tags.all():
            all_translations = loads(tag.tag_translations)
            tag_translations[tag.name] = all_translations
        response_answers.append({
            "msgid": answer.msgid,
            "blockedAnswers": blocked_answers,
            "mediaSourcePath": answer.mediaSourcePath,
            "mediaGroup": answer.mediaGroup,
            "tags": tag_slugs,
            "tag_translations": tag_translations,
        })
    return {
        "question": model_to_dict(question, fields=('id', 'msgid', 'isMultipleChoice', 'additionalInfo', 'isMediaQuestion')),
        "category": model_to_dict(question.category),
        "answers":  response_answers
    }
