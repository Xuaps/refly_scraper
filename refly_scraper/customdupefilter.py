import os
from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from scrapy.http import Request

class CustomFilter(RFPDupeFilter):

    def __getid(self, url):
        if url.find('?') != -1:
            mm = url.split("?")[0]
        elif url.find('$') != -1:
            mm = url.split("$")[0]
        elif url.find('#') != -1:
            mm = url.split("#")[0]
        else:
            mm = url
        return mm


    def request_seen(self, request):
        fp = request_fingerprint(Request(self.__getid(request.url)))
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
