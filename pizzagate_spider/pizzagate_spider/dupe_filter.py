import re
from scrapy.dupefilters import RFPDupeFilter
#from scrapy.utils.request import request_fingerprint

dup_links = r'(https?://www\.reddit\.com/r/\w+/comments/\w+/\w+/)|(https?://www\.thelastamericanvagabond\.com/.+/.+/)'

class CustomFilter(RFPDupeFilter):

	def request_fingerprint(self, request):
		mm = re.search(dup_links, request.url)
		return request.url if mm is None else mm.group(0)