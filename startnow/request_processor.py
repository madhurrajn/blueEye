import logging 
import ssl
import simplejson
import urllib2

logger = logging.getLogger(__name__)

class RequestProcessor:
    def __init__(self, url_list):
        self.url_list = url_list

    def process_requests(self):
        duration_list = []
        idx = 0
        context = ssl._create_unverified_context()
        ''' Shall be handled to set parallel requests '''
        for url in self.url_list:
            idx = idx + 1
            response = simplejson.load(urllib2.urlopen(url, context=context))
            status = response['status']
            if status == "OK":
                logger.info("Response Successfull")
                row = response['rows']
                for row_elem in row:
                    elems = row_elem['elements']
                    for e in elems:
                        duration = e['duration_in_traffic']['text']
                        logger.info(
                            "Duration taken for url {} is {}".format(url, duration))
                        duration_list.append((idx, duration))
            else:
                duration_list.append((idx, 0))
        return duration_list


