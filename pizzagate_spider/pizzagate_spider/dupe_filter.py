import re
from scrapy.dupefilters import RFPDupeFilter
#from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):

    def request_fingerprint(self, request):
        mm = re.search(r'https?://www.reddit.com/r/\w+/comments/\w+/\w+/', request.url)
        return request.url if mm is None else mm.group(0)