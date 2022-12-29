from django.core.management.base import BaseCommand, CommandError
from distrochooser.models import Distribution, ResultDistroSelection
from distrochooser.calculations.default import get_statistics

class Command(BaseCommand):
    help = 'Updates the distribution stats'

    def handle(self, *args, **options):
        distros = Distribution.objects.all()
        percentages = {}
        distro: Distribution
        for distro in distros:
            id = distro.id
            percentage, positive_votes, all_votes = get_statistics(id)
            distro.percentage = percentage
            distro.ratings = all_votes
            distro.positive_ratings = positive_votes
            percentages[id] = percentage

                
        percentages = {k: percentages[k] for k in sorted(percentages, key=percentages.get, reverse=True)}
        distro: Distribution
        for distro in distros:
            rank = list(percentages.values()).index(percentages[distro.id]) + 1 # starting with 0
            distro.rank = rank
            distro.save()
        