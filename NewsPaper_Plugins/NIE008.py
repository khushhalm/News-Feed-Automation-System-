from GenericCrawlerandExtractor import GCA
from InputMethods import input_json

CONFIG_PATH = '/home/hp/NFA-System/Modules/NewsPaper_configs/'
CONFIG_FILE = 'configs_NIE.json'


class NIE(GCA):
    def __init__(self, **kwargs):
        self.source_configs = {}
        self.source_configs.update(kwargs)
        config_data = input_json(path=CONFIG_PATH, file_name=CONFIG_FILE)
        self.source_configs['extractor_configs'] = config_data
        super().__init__(**self.source_configs)
        self.xml_tree = super().convertresponsetoxmltree()

    def getarticleidfromurl(self):
        article_id = self.source_configs.get("url").split("-")[-1].split(".")[0]
        return article_id


def getsourceresponse():
    kwargs={}
    url = 'https://www.newindianexpress.com/states/tamil-nadu/2020/oct/11/no-virus-can-escape-eyes-oftrichygovernment-medical-colleges-wonder-women-2208725.html'
    kwargs['url'] = url
    obj = NIE(**kwargs)
    return obj.getarticleidfromurl()

getsourceresponse()