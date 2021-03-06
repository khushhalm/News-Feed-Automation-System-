from GenericCrawlerandExtractor import GCA
from InputMethods import input_json
import json
import re

CONFIG_PATH = '/home/hp/NFA-System/Modules/NewsPaper_configs/'
CONFIG_FILE = 'configs_TOI.json'


class TOI(GCA):
    def __init__(self, **kwargs):
        self.source_configs = {}
        self.source_configs.update(kwargs)
        config_data = input_json(path=CONFIG_PATH, file_name=CONFIG_FILE)
        self.source_configs['extractor_configs'] = config_data
        super().__init__(**self.source_configs)
        self.xml_tree = super().convertresponsetoxmltree()

    def getarticleidfromurl(self):
        article_id = self.source_configs.get("url").split("/articleshow/")[-1].split(".")[0]
        return article_id

    def getjsonobject(self):
        article_response = super().return_reponse()
        json_string = re.search("window.App=(.*?)</script><script>", article_response).group(1)
        json_obj = json.loads(json_string)

        return json_obj

    def extractarticlebody_json(self):
        article_id = self.getarticleidfromurl()
        json_dict = self.getjsonobject()
        story_list = json_dict.get("state", {}).get("articleshow", {}).get("data", {}).get(str(article_id), {})\
            .get("story", [])
        story =[]
        for items in story_list:
            if items.get("tn") in ['text', 'keywoard']:
                story.append(items.get("value"))

        return story

    def extractkeywords_json(self):
        article_id = self.getarticleidfromurl()
        json_dict = self.getjsonobject()
        keywords = json_dict.get("state", {}).get("articleshow", {}).get("data", {}).get(str(article_id), {}).get("kws", '')

        return keywords

    def extractimagelink_json(self):
        base_url ='https://static.toiimg.com/thumb/msid-'
        image_url =base_url +str(self.getarticleidfromurl()) + ',imgsize-162203/photo.jpg'
        return image_url


def getsourceresponse():
    kwargs={}
    url = 'https://timesofindia.indiatimes.com/city/chennai/covid-doubling-time-up-viral-spread-slows-down/articleshow/78609430.cms'
    kwargs['url'] = url
    obj = TOI(**kwargs)
    return obj.getarticleidfromurl()


getsourceresponse()