from distrochooser.constants import TRANSLATIONS
from distrochooser.models import  GivenAnswer, ResultDistroSelection, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix, UserSession
from django.forms.models import model_to_dict
from django.db import transaction
from django.db.models import Q
from typing import Tuple

def saveAnswers(userSession, rawAnswers):
  # Delete old answers
  GivenAnswer.objects.filter(session=userSession).delete()
  newAnswers = []
  selectedAnswers = {answer[0]: answer[1] for answer in Answer.objects.filter(msgid__in=[a["msgid"] for a in rawAnswers]).values_list('msgid', 'pk')}
  for answer in rawAnswers:
    newAnswers.append(
      GivenAnswer(
          session=userSession,
          answer_id=selectedAnswers[answer['msgid']],
          isImportant=answer['important'],
          isLessImportant=answer['lessImportant']
      )
    )
  received = GivenAnswer.objects.bulk_create(newAnswers)
  answer: GivenAnswer
  for answer in received:
    raw_objs = list(filter(lambda a: a["msgid"] == answer.answer.msgid, rawAnswers))
    if len(raw_objs) == 1:
      answer.save()
      if "tags" in raw_objs[0]:
        tags = raw_objs[0]["tags"]
        for tag in tags:
          answer.tags.add(tag)
      answer.save()

def get_statistics(distro_id: int) -> Tuple[float, int, int]:
  """
  Returns the percentage of approval for the given distro

  Returns:
    A tuple of the percentage, the amount of positive votes and the overall vote count.
    Meaning of the first value:
    positive float: More users approve this selections
    negative float: More user disapprove this result
    50: Equal count of approvals/ disapprovals
    0: No ratings yet
  """
  
  # Get all voted results for this distribution
  selections = ResultDistroSelection.objects.filter(distro=distro_id).filter(Q(isApprovedByUser=True) | Q(isDisApprovedByUser=True))

  approved_by_user= selections.filter(isApprovedByUser=True).count()
  all_count = selections.count()
  not_approved_by_user = all_count - approved_by_user
  percentage = 0
  if approved_by_user > 0:
    percentage = (100/(all_count/ approved_by_user)) if approved_by_user != 0 else 0
  elif not_approved_by_user == approved_by_user and approved_by_user == 0:
    percentage = 0
  elif not_approved_by_user == approved_by_user:
    percentage = 50
  else:
    percentage = -1 * (100/(all_count/ not_approved_by_user)) if not_approved_by_user != 0 else 0

  return round(percentage,0), approved_by_user, all_count

@transaction.atomic
def getSelections(userSession: UserSession, data, langCode):
  translationToUse = TRANSLATIONS[langCode] if langCode in TRANSLATIONS else TRANSLATIONS["en"]
  ResultDistroSelection.objects.filter(session=userSession).delete()
  saveAnswers(userSession, data['answers'])
  givenAnswers = GivenAnswer.objects.filter(session=userSession).prefetch_related('answer').values("answer","isImportant", "isLessImportant")
  importantAnswers = list(map(lambda o: o["answer"], filter(lambda o: o["isImportant"], givenAnswers)))
  lessImportantAnswers = list(map(lambda o: o["answer"], filter(lambda o: o["isLessImportant"], givenAnswers)))
  distros = Distribution.objects.all()
  matchingTuples = AnswerDistributionMatrix.objects.filter(isSuggestion=False).prefetch_related('distros', 'answer')


  createdSelections = {}
  createdReasons = {}

  hardware_requirements = {
    "hardware_cores": userSession.hardware_cores,
    "hardware_frequency": userSession.hardware_frequency,
    "hardware_memory": userSession.hardware_memory,
    "hardware_storage": userSession.hardware_storage,
    "hardware_has_touch_support": userSession.hardware_is_touch,
  }
  do_hardware_check = True
  for key, value in hardware_requirements.items():
    if value == -1:
      do_hardware_check = False
      break
  hardware_requirements_translations = {
    "hardware_cores": "hardware-cpu-cores-title",
    "hardware_frequency": "hardware-cpu-frequency-title",
    "hardware_memory": "hardware-memory-title",
    "hardware_storage": "hardware-storage-title",
    "hardware_has_touch_support": "hardware-touch-title",
  }

  newSelections = []
  matchedTags = {}
  for distro in distros:
    selection = ResultDistroSelection(
      session=userSession,
      distro=distro
    )
    newSelections.append(selection)
    createdSelections[distro.id] = selection
    createdReasons[distro.id] = []
    selection.save()

  matrixTuple: AnswerDistributionMatrix
  for matrixTuple in matchingTuples:
    isInAnswerList = matrixTuple.answer.pk in (o["answer"] for o in givenAnswers)
    if isInAnswerList:
      matchedGivenAnswer = GivenAnswer.objects.filter(session=userSession, answer=matrixTuple.answer).first()
      selectedDescription = translationToUse[matrixTuple.description] if matrixTuple.description in translationToUse else matrixTuple.description

      reason = SelectionReason(
        isImportant = matrixTuple.answer.pk in importantAnswers,
        isLessImportant = matrixTuple.answer.pk in lessImportantAnswers,
        resultSelection = None,
        isBlockingHit = matrixTuple.isBlockingHit,
        isPositiveHit = not matrixTuple.isNegativeHit if not matrixTuple.isNeutralHit else True,
        isNeutralHit = matrixTuple.isNeutralHit,
        description = selectedDescription
      )
      
      # prevent that same descritptions appear multiple times
      isReasonUnique = not len(list(filter(lambda r: r.description == reason.description, createdReasons[distro.id]))) > 0
      
      for distro in matrixTuple.distros.all():
        # verify peculiarities to match with the distribution
        got = distro.tags.filter(name__in=matchedGivenAnswer.tags.names())
        new_tags = list(got.values_list("name",flat=True))
        if distro.id not in matchedTags:
          matchedTags[distro.id] = new_tags
        else:
          matchedTags[distro.id] = matchedTags[distro.id] + new_tags
        
        # Make sure tehere are no double entries
        matchedTags[distro.id] = list(set(matchedTags[distro.id]))
        if isReasonUnique:
          selection = createdSelections[distro.id]
          # Tag Only hits are used to return the tags to the user result.
          # But these answers are not included in a decision making
          if not matrixTuple.isTagOnlyHit:
            reason.resultSelection = selection
            createdReasons[distro.id].append(reason)
            reason.save()
  results = []
  for distroId, selection in createdSelections.items():
    reasons = createdReasons[distroId]
    requirements_check_result = {}
    requirements_check_values = {}
    has_failed_requirements_check = False
    if selection.distro.hardware_requirements_present and do_hardware_check:
      for key, user_requirement_value in hardware_requirements.items():
        distro_value = getattr(selection.distro, key)
        is_fullfilled = False
        is_needed = True
        if "has" in key:
          # only check booleans if the user demands it
          if user_requirement_value:
            is_fullfilled = distro_value == True
          else:
            is_needed = False
        else:
          is_fullfilled = distro_value <= user_requirement_value
        if is_needed:
          translation_key = hardware_requirements_translations[key]
          if not is_fullfilled:
            has_failed_requirements_check = True
          requirements_check_result[translation_key] = is_fullfilled
          requirements_check_values[translation_key] = [
            distro_value if "has" not in key else translationToUse["boolean-" + str(distro_value).lower()],
            user_requirement_value
          ]
      
      hardware_check_reason = SelectionReason(
        isImportant = False,
        resultSelection = selection,
        isBlockingHit = has_failed_requirements_check,
        isPositiveHit = not has_failed_requirements_check,
        isNeutralHit = False,
        description = translationToUse["hardware-check-failed" if has_failed_requirements_check else "hardware-check-succeeded"]
      )
      hardware_check_reason.save()
      reasons.append(hardware_check_reason)
    
    add_condition = selection.distro.hardware_requirements_present and requirements_check_result and not has_failed_requirements_check if userSession.filter_by_hardware else True
    if add_condition:
      results.append(
        {
          "did_hardware_check": selection.distro.hardware_requirements_present,
          "hardware_check": requirements_check_result,
          "failed_hardware_check": has_failed_requirements_check,
          "requirements_check_values": requirements_check_values,
          "distro": model_to_dict(selection.distro, exclude=["logo", "tags"]),
          "reasons": list(map(lambda r: model_to_dict(r,exclude=["id", "isDisApprovedByUser"]), reasons)),
          "selection": selection.id,
          "tags": matchedTags[distroId] if distroId in matchedTags else [],
          "percentage": selection.distro.percentage,
          "positive_ratings": selection.distro.positive_ratings,
          "ratings": selection.distro.ratings,
          "rank": selection.distro.rank
        }
      )
  return results