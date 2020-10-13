from CommonFunctions import parserssfeedresponse, extractrssresponse
import logging
logging.basicConfig(level=logging.INFO)

sources=['Business Standard', 'Livemint', 'Times of India', 'The Hindu',
         'The New Indian Express', 'Dailythanthi', 'Dinakaran,Dinamani', 'Hindu thamil thisai']


class RssFeedExtractor:
    def __init__(self, **kwargs):
        self.values={}
        self.values.update(kwargs)

    def getrssfeeds(self):
        if self.values.get("rss_url", False):
            source_id = self.values.get("source_id")
            feed = (self.values.get("rss_url"))
            feed_details = self.values.get("input_data", {}).get(source_id, {}).get(feed, {})
            # rss_feed_list= {self.values.get("source_id"): (self.values.get("rss_url"))}
            # feed_details = self.values.get("rss_url")
            rss_feed_list = {source_id: {feed: feed_details}}
            return rss_feed_list
        else:
            rss_feed_list = self.values.get("input_data", {})
        return rss_feed_list

    def extractarticlelinks(self):
        inputfeeds = self.getrssfeeds()
        for source, feed_data in inputfeeds.items():
            for feed, details in feed_data.items():
                # feed_details =self.values.get("input_data", {}).get("rss_details", {}).get(feed, {})
                rss_response = parserssfeedresponse(feed=feed, feed_language=details.get("newspaper_language"))
                feed_response = extractrssresponse(response=rss_response,
                                                  timeline_start_date=self.values.get("timeline_start_date"),
                                                  timeline_start_hour=self.values.get("timeline_start_hour"))
                logging.info("RSS Feed : " + str(feed) + ". Feed details extracted :\nMetadata : " +
                            str(feed_response.get("metadata")) +
                             "\nNumber of article links found within the extracted timeline :"
                             + str(len(feed_response.get("article_links")))+"\n\n")
                details.update(feed_response)

        return inputfeeds


def getsourceobj(**kwargs):
    obj=RssFeedExtractor(**kwargs)
    response_data = obj.extractarticlelinks()
    return response_data
