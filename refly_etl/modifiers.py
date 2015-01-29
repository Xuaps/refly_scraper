import urllib,  demjson
import re
import csv
from metl.utils import *

class ReplaceByDictFile( Modifier ):

    init = ['file','field','regex']

    def __init__( self, reader, file, field, regex = '\n   (\[\d*\]: [\.:?=/\w\-#~,\.; \*\@\(\)]*)', *args, **kwargs ):

        self.regex = regex.decode('utf-8')
        self.field = field.decode('utf-8')
        with open(file, mode='r') as infile:
            file_reader = csv.reader(infile, delimiter='|')
            self.urls = {rows[0]:rows[1].decode('utf-8') for rows in file_reader}
        super( ReplaceByDictFile, self ).__init__( reader, *args, **kwargs )

    # FieldSet
    def modify( self, record ):
        content = unicode(record.getField(self.field).getValue())
        for match in re.findall(self.regex,content):
            keymatch = self.get_url(match)
            if keymatch in self.urls:
                content = content.replace(match, self.get_url_number(match)+self.urls[keymatch], 1)
                record.getField(self.field).setValue(content)
        return record
    
    def get_url(self, match):
        sanitized = match[match.find(': ')+2:] 
        if sanitized.find('#')!=-1:
            sanitized = sanitized[:sanitized.find('#')]

        return sanitized

    def get_url_number(self, match):
        return match[:match.find(': ')+2]

class RepairLinks( Modifier ):

    init = ['file','field','regex']

    def __init__( self, reader, file, field, regex = None, *args, **kwargs ):
        self.regex = regex.decode('utf-8')
        self.field = field.decode('utf-8')
        self.urls = []
        with open(file, mode='r') as infile:
            file_reader = csv.reader(infile, delimiter=',')
            for rows in file_reader:
                self.urls.append({'code': rows[0],'origin': rows[1],'final': rows[2]})

        super( RepairLinks, self ).__init__( reader, *args, **kwargs )

    # FieldSet
    def modify( self, record ):
        content = unicode(record.getField(self.field).getValue())
        for uri in self.urls:
            link_re = re.compile("\[\d*\]: (" + self.escape_chars(uri['origin']) + ")")
            for match in re.findall(link_re,content):
                if uri['code'] =='301':
                    content = content.replace(match, self.escape_chars(uri['final']),1)
                elif uri['code'] =='404':
                    content = content.replace(match, '/searchfor/' + match.split('/')[-1],1)
        record.getField(self.field).setValue(content)
        return record

    def escape_chars(self,text):
        return text.replace('(', '\(').replace(')', '\)')


class UniqueField( Filter ):
    included = []
    init = ['field']

    def __init__( self, reader, field, *args, **kwargs ):

        self.field = field
        super( UniqueField, self ).__init__( reader, *args, **kwargs )
    # bool
    def isFiltered( self, record ):
        
        key = record.getField(self.field).getValue()

        if key in self.included:
            return True

        self.included.append(key)
        return False
