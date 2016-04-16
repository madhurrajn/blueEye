import time

import logging 

logger = logging.getLogger(__name__)

SECONDS_IN_HOUR=3600

class UrlProcessor:
    def __init__(self, orig_lat, orig_lng, dest_lat, dest_lng):
        self.orig_lat = orig_lat
        self.orig_lng = orig_lng
        self.dest_lat = dest_lat
        self.dest_lng = dest_lng
        # self.ref_string="https://www.google.co.in/maps/preview/directions?authuser=0&hl=en&pb=!1m5!1s12.8857037%2C77.566548!3m2!3d12.885703699999999!4d77.566548!6e2!1m5!1s12.9394137%2C77.69520310!3m2!3d12.9394137!4d77.6952031!6e2!2e0!3m12!1m3!1d120719.55006746609!2d77.62934954999999!3d12.910809949999996!2m3!1f0!2f0!3f0!3m2!1i706!2i745!4f13.1!6m14!1m0!2m3!5m1!2b0!20e3!10b1!16b1!19m3!1e0!2e2!3j1460736000!20m2!1e0!2e3!8m0!15m4!1sfogQV4rFGIeajwPAzI3QAQ!4m1!2i7296!7e81!20m0!27b1!28m0"
        self.ref_string = "https://maps.googleapis.com/maps/api/distancematrix/json?origins='Mysore'&destinations='Bangalore'&mode=driving&departure_time=now&key=AIzaSyCO9qZ4EGkX9xU7-n4r2v6u9AGk4_j6Kk4"
        # self.static_string="https://www.google.co.in/maps/preview/directions?authuser=0&hl=en&pb=!1m5!1sORIG_LAT_LONG!3m2!3dORIG_LAT!4dORIG_LNG!6e2!1m5!1sDEST_LAT_LONG!3m2!3dDEST_LAT!4dDEST_LNG!6e2!2e0!3m12!1m3!1d120719.55006746609!2d77.62934954999999!3d12.910809949999996!2m3!1f0!2f0!3f0!3m2!1i706!2i745!4f13.1!6m14!1m0!2m3!5m1!2b0!20e3!10b1!16b1!19m3!1e0!2e2!3jDEPARTAT!20m2!1e0!2e3!8m0!15m4!1sfogQV4rFGIeajwPAzI3QAQ!4m1!2i7296!7e81!20m0!27b1!28m0"
        self.static_string = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=ORIG_LAT_LNG&destinations=DEST_LAT_LNG&mode=driving&departure_time=DEPARTAT&key=AIzaSyCO9qZ4EGkX9xU7-n4r2v6u9AGk4_j6Kk4"

    def get_lat_long_url(self):
        str = self.static_string.replace(
            "ORIG_LAT_LNG", self.orig_lat + "," + self.orig_lng)
        str = str.replace("DEST_LAT_LNG", self.dest_lat + "," + self.dest_lng)
        return str

    def get_curr_time(self):
        return int(time.time())

    def update_time_in_url(self, url, time):
        url = url.replace("DEPARTAT", str(time))
        return url

    def create_url_list(self, url, count, curr_time, delta):
        url_list = []
        logger.info("url {}, count {}, curr_time {}, delta {}".format(url, count, curr_time, delta))
        actual_time = curr_time
        for i in range(1,count):    
            logger.info("Processing url {}".format(i))
            url_str = self.update_time_in_url(url, actual_time)
            url_list.append(url_str)
            actual_time = actual_time + delta
        return url_list

    def create_url(self, range, count):
        url_str = self.get_lat_long_url()
        url_count = range*SECONDS_IN_HOUR/count
        logger.info("URL Str with Lat Long info {} url_count {}".format(url_str, count))
        curr_time = self.get_curr_time()
        url_list = self.create_url_list(url_str, int(count), curr_time, SECONDS_IN_HOUR)
        return url_list

