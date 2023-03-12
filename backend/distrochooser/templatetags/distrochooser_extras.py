from django import template
from distrochooser.models import Distribution, AnswerDistributionMatrix, Answer, UserSuggestion
register = template.Library()

@register.inclusion_tag('tag_distro.html')
def tag_distro(distro: Distribution, matrix_tuple: AnswerDistributionMatrix, answer: Answer, suggestion: UserSuggestion = None ):
    return {'distro': distro, 'matrix_tuple': matrix_tuple, 'answer': answer, 'suggestion': suggestion}


@register.inclusion_tag('tag_selection.html')
def tag_selection(matrix_tuple: AnswerDistributionMatrix, answer: Answer):
    return {'matrix_tuple': matrix_tuple, 'answer': answer}