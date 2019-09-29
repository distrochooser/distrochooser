from django.core.management.base import BaseCommand, CommandError
from distrochooser.models import UserSession
from django.db.models import Count
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
      visitors = UserSession.objects.filter(dateTime__gte=datetime.now()-timedelta(days=7)).order_by("dateTime")
      backlinks = UserSession.objects.filter(referrer__isnull=False, dateTime__gte=datetime.now()-timedelta(days=7)).values('referrer').annotate(total=Count('referrer')).order_by('total').values("referrer","total")
      import asciichartpy
      data = {}
      finishedTests = {}
      for visitor in visitors:
        dateString = visitor.dateTime.strftime("%Y-%m-%d")
        if dateString in data:
          data[dateString] = data[dateString] + 1
        else:
          data[dateString] = 1
        if visitor.checksDone > 0:
          if dateString in finishedTests:
            finishedTests[dateString] = finishedTests[dateString] + 1
          else:
            finishedTests[dateString] = 1
      print("Last 7 days statistics")
      print("Visitors", data)
      print("Finished tests", finishedTests)
      print("Backlinks", list(backlinks))