import logging 
import ssl
import simplejson
import urllib2
import datetime
from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger(__name__)

class RequestProcessor:
    def __init__(self, url_list):
        self.url_list = url_list
        self.duration_list = []

    def process_atomic_request(self, (atime, url)):
        context = ssl._create_unverified_context()
        response = simplejson.load(urllib2.urlopen(url, context=context))
        status = response['status']
        utime =  datetime.datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S')
        if status == "OK":
            logger.info("Response Successfull")
            row = response['rows']
            for row_elem in row:
                elems = row_elem['elements']
                for e in elems:
                    duration = e['duration_in_traffic']['text']
        return (utime, duration)

    def process_async_requests(self, url_list):
        pool = ThreadPool(len(url_list))
        result = pool.map(self.process_atomic_request, url_list)
        pool.close()
        pool.join()
        return result

    def process_requests(self, url_list):
        return (self.process_async_requests(url_list))

