from django.core.management.base import BaseCommand
from distrochooser.models import Distribution, Answer, AnswerTag
from distrochooser.calculations.default import get_statistics
from requests import get
from time import sleep

from django.utils.text import slugify
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
from slugify import slugify
from backend.settings import LOCALES_PATH
from json import dumps

class Command(BaseCommand):
    help = 'Updates the distribution stats'
    def get_json(self, url: str) -> any:
        return get(url).json()
    def query_data(self, id: str):
        statement_map = {
            "founded":  ["P571",  "P577"],
            "desktops": ["P1414"],
            "version": ["P348"],
            "license": ["P275"],
            "packagemgmt": ["P3033"],
            "arch": ["P400"],
            "language": ["P407"]
        }
        transform_map = {
            "P571": lambda e: e["time"],
            "P577": lambda e: e["time"],
            "P1414": lambda e:  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+e["id"]+ ".json")["entities"][e["id"]]["labels"]["en"]["value"],
            "P3033": lambda e:  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+e["id"]+ ".json")["entities"][e["id"]]["labels"]["en"]["value"],
            "P275": lambda e:  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+e["id"]+ ".json")["entities"][e["id"]]["labels"]["en"]["value"],
            "P400": lambda e:  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+e["id"]+ ".json")["entities"][e["id"]]["labels"]["en"]["value"],
            "P407": lambda e:  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+e["id"]+ ".json")["entities"][e["id"]]["labels"]["en"]["value"],
        }
        results = {}
        translations = {}

        to_translate = ["language","arch", "packagemgmt", "license"]

        origin_json = self.get_json(f"https://www.wikidata.org/wiki/Special:EntityData/{id}.json")
        for key, value in statement_map.items():
            root = origin_json["entities"][id]["claims"]
            for option in value:
                result = root.get(option)
                results[key] = list()
                if result:
                    for tuple in result:
                        raw_value = tuple["mainsnak"]["datavalue"]["value"]
                        tag_result = slugify(raw_value if option not in transform_map else transform_map[option](raw_value))
                        if option in transform_map and key in to_translate:
                            entry_id = raw_value["id"]
                            print(f"Parsing {option}, links to {entry_id} ()")
                            translation_json =  self.get_json("https://www.wikidata.org/wiki/Special:EntityData/"+entry_id+ ".json")
                            labels = translation_json["entities"][entry_id]["labels"]
                            for lang_code, value in labels.items():
                                if lang_code not in translations:
                                    translations[lang_code] = {}
                                translation_key = f"tag-{key}-{tag_result}"
                                value = value["value"]
                                if tag_result not in translations[lang_code]:
                                    translations[lang_code][translation_key] = value

                        results[key].append(tag_result)

                    

        return results, translations
    
    def handle(self, *args, **options):
        distros = Distribution.objects.all()
        clicks = {}
        seen_translations = {}
        distro: Distribution
        for distro in distros:
            print("Processing " + distro.name)
            id = distro.id
            percentage, positive_votes, all_votes = get_statistics(id)
            distro.percentage = percentage
            distro.ratings = all_votes
            distro.positive_ratings = positive_votes
            clicks[id] = distro.clicks
            distro: Distribution
            if distro.data_id:
                data, translations = self.query_data(distro.data_id)

                for lang_code, values in translations.items():
                    for tag_name, value in values.items():
                        if tag_name not in seen_translations:
                            seen_translations[tag_name] = {}
                        
                        if lang_code not in seen_translations[tag_name]:
                            seen_translations[tag_name][lang_code] = value


                distro.metric_translations = dumps(translations)
                taggable = ["desktops", "license", "packagemgmt", "arch",  "language"]
                for tag in taggable:
                    tag_values = data[tag]
                    for tag_value in tag_values:
                        db_value = slugify(f"{tag}-{tag_value}")
                        distro.tags.add(db_value)

                for meta_info in ["version", "founded"]:
                    if meta_info in data and len(data[meta_info]) > 0:
                        distro.__setattr__(meta_info, data[meta_info][-1])
                if distro.founded:
                    if "00-00" in distro.founded:
                        distro.founded = distro.founded.replace("00-00", "01-01")
                    if "-00" in distro.founded:
                        distro.founded = distro.founded.replace("-00", "-01")
                    if "t" in distro.founded:
                        distro.founded =  distro.founded.split("t")[0]
                    parsed = dateutil.parser.parse(distro.founded.replace("+",""))
                    distro.founded = parsed.date()
                    now = datetime.date.today()
                    age = relativedelta(now, distro.founded).years
                    distro.age = age
                distro.save()
                sleep(2)



        clicks = {k: clicks[k] for k in sorted(clicks, key=clicks.get, reverse=True)}


        distro: Distribution
        for distro in distros:
            rank = list(clicks.values()).index(clicks[distro.id]) + 1 if distro.id in clicks  else 0 
            distro.rank = rank
            distro.save()

        all_tags = AnswerTag.objects.all()

        tag: AnswerTag
        for tag in all_tags:
            needle = f"tag-{tag.tag.name}"
            if needle in seen_translations:
                tag.tag.tag_translations = dumps(seen_translations[needle])
                tag.tag.save()

        for answer in Answer.objects.all():
            if answer.tag_prexfix:
                for tag in all_tags:
                    if tag.tag.name.startswith(answer.tag_prexfix):
                        answer.tags.add(tag.tag.name)
            answer.save()
        