from collections import defaultdict
import itertools

from distrochooser.constants import TRANSLATIONS
from distrochooser.models import GivenAnswer, ResultDistroSelection, Distribution, SelectionReason, Answer, AnswerDistributionMatrix
from django.forms.models import model_to_dict


def save_answers(user_session, raw_answers):
    GivenAnswer.objects.filter(session=user_session).delete()
    answer_map = dict(Answer.objects.filter(msgid__in=[a["msgid"] for a in raw_answers]).values_list('msgid', 'pk'))

    given_answers_to_create = []

    for answer in raw_answers:
        given_answers_to_create.append(
            GivenAnswer(
                session=user_session,
                answer_id=answer_map[answer['msgid']],
                isImportant=answer['important']
            )
        )

    GivenAnswer.objects.bulk_create(given_answers_to_create)

    return given_answers_to_create


def get_selections(user_session, data, lang_code):
    translation_to_use = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])
    ResultDistroSelection.objects.filter(session=user_session).delete()
    given_answers = save_answers(user_session, data["answers"])

    important_answers = [ga.answer_id for ga in given_answers if ga.isImportant]
    matching_tuples = AnswerDistributionMatrix.objects.prefetch_related("distros").all()
    reasons_by_selection = defaultdict(list)

    result_distro_selection = [
        ResultDistroSelection(
            session=user_session,
            distro=distro
        ) for distro in Distribution.objects.all()
    ]

    ResultDistroSelection.objects.bulk_create(result_distro_selection)

    created_selections = {selection.distro_id: selection for selection in result_distro_selection}

    for matrix_tupel in matching_tuples:
        if matrix_tupel.answer_id not in [ga.answer_id for ga in given_answers]:
            continue

        selected_description = translation_to_use.get(matrix_tupel.description, matrix_tupel.description)

        reason_base = {
            "isImportant": matrix_tupel.answer_id in important_answers,
            "isBlockingHit": matrix_tupel.isBlockingHit,
            "isPositiveHit": matrix_tupel.isNeutralHit or not matrix_tupel.isNegativeHit,
            "isNeutralHit": matrix_tupel.isNeutralHit,
            "description": selected_description
        }

        for distro in matrix_tupel.distros.all():
            selection = created_selections[distro.pk]

            if reason_base["description"] not in [added_reason.description for added_reason in reasons_by_selection[selection.id]]:
                reasons_by_selection[selection.id].append(
                    SelectionReason(resultSelection=selection, **reason_base)
                )

    SelectionReason.objects.bulk_create(list(itertools.chain(*reasons_by_selection.values())))

    results = []

    for selection in created_selections.values():
        reasons = reasons_by_selection[selection.id]
        results.append(
            {
                "distro": model_to_dict(selection.distro, exclude=["logo", "id"]),
                "reasons": [model_to_dict(r, exclude=["id", "resultSelection"]) for r in reasons],
                "selection": selection.id
            }
        )

    return results
