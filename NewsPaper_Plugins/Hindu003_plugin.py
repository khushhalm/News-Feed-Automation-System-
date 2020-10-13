from GenericCrawlerandExtractor import GCA
from InputMethods import input_json

CONFIG_PATH = '/home/hp/NFA-System/Modules/NewsPaper_configs/'
CONFIG_FILE = 'configs_The Hindu.json'


class Hindu(GCA):
    def __init__(self, **kwargs):
        """
        kwargs:
            url : The article link
            source_id : Source id for Hindus
            articleody,keyword,images : extraction type and configuration  e.g "articlebody" : {"xpath" : "//div[@class='body']"
            }
        """
        self.source_configs ={}
        self.source_configs.update(kwargs)
        config_data = input_json(path=CONFIG_PATH, file_name=CONFIG_FILE)
        self.source_configs['extractor_configs'] =config_data
        super().__init__(**self.source_configs)
        self.xml_tree = super().convertresponsetoxmltree()

    def getarticleidfromurl(self):
        article_id = self.source_configs.get("url").split("/article")[-1].split(".")[0]
        return article_id

    def extractarticlebody_xml(self):
        a_id = self.getarticleidfromurl()
        xpath = "//div[@id='content-body-14269002-" + str(a_id) + "']//text()"
        article_body = self.xml_tree.xpath(xpath)
        return article_body


def getsourceresponse():
    kwargs={}
    url = 'https://www.thehindu.com/news/national/tamil-nadu/more-number-of-high-court-judges-opt-for-physical-hearing-from-october-5/article32737045.ece'
    kwargs['url'] = url
    obj = Hindu(**kwargs)
    return obj.getarticleidfromurl()


getsourceresponse()