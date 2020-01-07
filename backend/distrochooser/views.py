"""
Views of the API backend.
"""

from json import loads
from secrets import token_hex
from base64 import b64decode

from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest, JsonResponse, Http404

from backend.settings import LOCALES
from distrochooser.util import get_json_response, get_step_data
from distrochooser.calculations import refactored, static
from distrochooser.models import UserSession, Category, ResultDistroSelection, GivenAnswer, AnswerDistributionMatrix
from distrochooser.constants import TRANSLATIONS, TESTOFFSET


def get_locales(request: HttpRequest) -> JsonResponse:
    """
    Returns a list of installed locales (ISO-639-1) as a JSON response

    Args:
      request (HttpRequest): The request of the client

    Returns:
      JsonResponse: An array of the installed locales
    """
    return get_json_response(list(LOCALES.keys()))


def getStats(request):
    # this method is a stub and is not included in production.
    results = ResultDistroSelection.objects.all().values(
        'session_id').annotate(total=Count('session_id')).filter(total__gt=0)
    approvedResults = ResultDistroSelection.objects.filter(
        isApprovedByUser=True)
    disapprovedResults = ResultDistroSelection.objects.filter(
        isDisApprovedByUser=True)
    allVoteResultsCount = approvedResults.count() + disapprovedResults.count()
    approvedPercentage = 0
    disApprovedPercentage = 0
    if allVoteResultsCount != 0:
        if approvedResults.count() != 0:
            approvedPercentage = round(
                100/(allVoteResultsCount/approvedResults.count()))
        if disapprovedResults.count() != 0:
            disApprovedPercentage = round(
                100/(allVoteResultsCount/disapprovedResults.count()))

    referrersQuery = UserSession.objects.values(
        "referrer").annotate(amount=Count('referrer'))
    referrers = {}
    for referrer in referrersQuery:
        backlink = referrer["referrer"]
        if backlink and "https://distrochooser.de" not in backlink and "https://beta.distrochooser.de" not in backlink:
            referrers[referrer["referrer"]] = referrer["amount"]

    return JsonResponse({
        "tests": results.count(),
        "visitors": UserSession.objects.all().count(),
        "votedResults": allVoteResultsCount,
        "approvedPercentage": approvedPercentage,
        "disApprovedPercentage": disApprovedPercentage,
        "referrers": referrers
    })


def get_ssr_data(request: HttpRequest, lang_code: str) -> HttpResponse:
    """
    Returns data needed to render it server side (e. g. about pages or meta tags)

    Args:
      request (HttpRequest): The client request
      lang_code (str): The language to use

    Returns:
      HttpResponse: A JSON serialized dataset of translated values
    """
    if lang_code not in TRANSLATIONS:
        raise Http404

    testCount = TESTOFFSET + UserSession.objects.all().count()
    responseData = TRANSLATIONS[lang_code].copy()
    responseData["testCount"] = testCount
    return JsonResponse(responseData)


def start(request: HttpRequest, lang_code: str, reflink_encoded: str) -> JsonResponse:
    """
    'Loggs' the visitor in, creates a session which will be used to store the user's action.

    Args:
      request (HttpRequest): The client request
      lang_code (str): The ISO-639-1 encoded language to use
      reflink_encoded (str): The base64 encoded referrer or "-"

    Returns:
      A JSON HTTP response containing 
      the token, the language, testCount, translations, questions, answers and categories
    """
    if lang_code not in LOCALES:
        raise Http404("Language not installed")

    user_agent = request.META["HTTP_USER_AGENT"]
    session = UserSession()
    session.userAgent = user_agent
    session.language = lang_code
    session.token = token_hex(5)  # generate a random token for the user
    session.checksToDo = AnswerDistributionMatrix.objects.all().count()
    session.save()
    if reflink_encoded != "-":
        reflink_decoded = b64decode(reflink_encoded).decode("utf-8")
        if reflink_decoded is not None:
            session.referrer = reflink_decoded
    session.save()
    view_bag_data = get_step_data(0)
    test_count = TESTOFFSET + UserSession.objects.all().count()
    return get_json_response({
        "token": session.token,
        "language": lang_code,
        "testCount": test_count,
        "translations": TRANSLATIONS[lang_code],
        "question": view_bag_data["question"],
        "category": view_bag_data["category"],
        "categories": list(Category.objects.all().order_by("index").values()),
        "answers": view_bag_data["answers"]
    })


def get_language_values(request: HttpRequest, lang_code: str) -> HttpResponse:
    """
    Receive language values as a JSON response.

    Args:
      request (HttpRequest): The client request
      lang_code (str): The language to use (ISO-639-1)

    Returns:
      HttpResponse: The JSON-encoded dictionary or a 404 error in case the language does not exist
    """
    if lang_code not in LOCALES:
        raise Http404("Language not installed")
    return get_json_response({
        "translations": TRANSLATIONS[lang_code]
    })


@csrf_exempt
def load_question(request: HttpRequest, index: int) -> JsonResponse:
    """
    Load a given answer by it's category index.

    May throw a 404 if the question/ category is not found.

    Args:
      request (HttpRequest): The client request
      index (int): The 0-based category index

    Returns:
      HttpResponse: The JSON response containing the question and the answer.
    """
    questionAndCategoryData = get_step_data(index)
    return get_json_response({
        "question": questionAndCategoryData["question"],
        "answers": questionAndCategoryData["answers"]
    })


@csrf_exempt
def submit_answers(request: HttpRequest, lang_code: str, token: str, method: str) -> HttpResponse:
    """
    Submit the user answers

    Args:
      request (HttpRequest): The client request. Contains the answers as application/json!
      lang_code (str): The ISO-639-1 encoded language to use
      token (str): The session token
      method (str): The calculation method to be used

    Returns:
      HttpResponse: Contains a JSON data of the result
    """
    if lang_code not in LOCALES:
        raise Exception("Language not installed")

    userSession = UserSession.objects.get(token=token)

    if userSession.isPending:
        return HttpResponse('A result is pending', status=409)

    userSession.isPending = True
    userSession.save(update_fields=["isPending"])

    data = loads(request.body)
    calculations = {
        "static": static.getSelections,
        "refactored": refactored.getSelections
    }
    if method in calculations:
        selections = calculations[method](userSession, data, lang_code)
    else:
        raise Exception("Calculation method not known")
    userSession.isPending = False
    userSession.save(update_fields=["isPending"])
    return get_json_response({
        "url": "https://beta.distrochooser.de/{0}/{1}/".format(lang_code, userSession.publicUrl),
        "selections": selections,
        "token": token
    })


@csrf_exempt
def vote(request: HttpRequest) -> HttpResponse:
    """
    Up-/ Downvote a selection for statistical purposes

    Args:
      request (HttpRequest): The client request (contains selection id as application/json)

    Returns:
      HttpResponse: A HTTP JSON response containing the count of tuples changed
    """
    data = loads(request.body)
    id = int(data["selection"])
    got = -1
    if data["positive"] is not None:
        isPositive = data["positive"] == True
        got = ResultDistroSelection.objects.filter(pk=id).update(
            isApprovedByUser=isPositive,
            isDisApprovedByUser=not isPositive
        )
    else:
        got = ResultDistroSelection.objects.filter(pk=id).update(
            isApprovedByUser=False,
            isDisApprovedByUser=False
        )

    return JsonResponse({
        "count": got
    })


@csrf_exempt
def update_remark(request: HttpRequest) -> JsonResponse:
    """
    Update the user remark on a User Session

    Args:
      request (HttpRequest): The client request
      the body is application/json to receive the fields result (int) and remarks (text)

    Returns:
      HTTP response with the count of the session results changed
    """
    data = loads(request.body)
    id = data["result"]
    remark = data["remarks"]
    oldSessionObject = UserSession.objects.get(token=id)
    got = -1
    # the remark can be changed once
    # to prevent that it can be overwritten when somebody get's a shared link
    if oldSessionObject.remarks is None:
        got = UserSession.objects.filter(token=id).update(remarks=remark)
    return get_json_response(got)


def get_given_answers(request: HttpRequest, token: str) -> JsonResponse:
    """
    Receive the answers of a given session token

    Args:
      request (HttpRequest): The client request
      token (str): The session token to search for

    Returns:
      JsonResponse: A dictionary (answers, important, categories) of the result
    """
    answers = GivenAnswer.objects.filter(session__publicUrl=token)
    answerList = []
    importanceList = []
    for answer in answers:
        answerList.append(answer.answer.msgid)
        if answer.isImportant:
            importanceList.append(answer.answer.msgid)
    return JsonResponse(
        {
            "answers": answerList,
            "important": importanceList,
            "categories": list(answers.values_list("answer__question__category__msgid", flat=True))
        }
    )
