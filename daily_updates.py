import configargparse
import InputMethods
import logging
import imp
import RssFeedExtractor
import NewsPaper_Plugins
import CustomErrors
import subprocess
from CommonFunctions import find_module


class DailyUpdates:
    def __init__(self, config_file=None):
        parser = configargparse.ArgParser()
        parser.add_argument('-c', '--config', required=False, is_config_file=True, help='config file path')
        parser.add_argument('--storage_path', required=False, type=str,
                            help='storage path for all TN daily updates file')
        parser.add_argument('--input_file', required=False, type=str,
                            help='Input file containing sources, ids, feed_ids etc. ')
        parser.add_argument('--db_connect', required=False, type=bool, help='Update to database')
        parser.add_argument('--run_aggr', required=False, type=bool,
                            help='Condition to run the rss fed aggregator {default: True}')
        parser.add_argument('--start_date', required=False, type=int,
                            help='Last number of days\' news should be craped {default : 1}')
        parser.add_argument('--start_hour', required=False, type=int,
                            help='hoto starur of the day to scraping {default : 0}')
        parser.add_argument('--start_min', required=False, type=int,
                            help='minute of the hour to start scraping {default :0 }')
        parser.add_argument('--aggr_limit', required=False, type=bool, help='to limit the aggregation of rss feeds')
        parser.add_argument('--aggr_limit_value', required=False, type=int, help='no of articles aggregation to limit')
        parser.add_argument('--rss_url', required=False, type=str, help='rss feed for aggregation')
        parser.add_argument('--article_url', required=False, type=str, help='article url for scraping')
        parser.add_argument('--run_extr', required=False, type=bool,
                            help='Condition to run the article extractor {default = True')
        parser.add_argument('--extr_limit', required=False, type=bool, help='to limit the extraction of article bodies')
        parser.add_argument('--extr_limit_value', required=False, type=int, help='no of article extraction to limit')
        parser.add_argument('--source_id', required=False, type=str, help='list of sources to run DailyUpdates')
        parser.add_argument('--test', required=False, type=bool, default=False,  help='unit testing')
        self.params=parser.parse_args()
        if self.params.rss_url and not self.params.source_id:
            raise CustomErrors.ConfigError

        self.input_data =InputMethods.input_json(path=self.params.storage_path, file_name=self.params.input_file)

    def run_aggregator(self):
        if not self.params.run_aggr:
            # db retrieval
            return 0
            # no db write
        else:
            kwargs ={'source_id': self.params.source_id, 'rss_url': self.params.rss_url, 'aggregator_limit': self.params.aggr_limit,
                     'aggregator_limit_value': self.params.aggr_limit_value, 'timeline_start_date':
                         self.params.start_date, 'timeline_start_hour': self.params.start_hour,
                     'input_data': self.input_data}
            rss_feeds = RssFeedExtractor.getsourceobj(**kwargs)
            # db_write
            return rss_feeds

    def run_extractor(self):
        #aggregated_data=self.run_aggregator()
        main_mod ='NewsPaper_configs'
        aggregated_data={'Hindu003': '1'}
        for source, data in aggregated_data.items():
            source_module =source +"_plugin"
            source_module = 'CommonFunctions'
            module =__import__(source_module)
            func =getattr(module, 'create_dummy_response')
            func()


obj= DailyUpdates()
obj.run_extractor()