import urllib, demjson
import re
import csv
from metl.utils import *

class ReplaceByDictFile( Modifier ):

    init = ['file','field','regex']

    def __init__( self, reader, file, field, regex = None, *args, **kwargs ):

        self.regex = regex
        self.field = field
        with open(file, mode='r') as infile:
            file_reader = csv.reader(infile, delimiter='|')
            self.urls = {rows[0]:rows[1] for rows in file_reader}

        super( ReplaceByDictFile, self ).__init__( reader, *args, **kwargs )

    # FieldSet
    def modify( self, record ):

        content=record.getField(self.field).getValue()
        for match in re.findall(self.regex,content):
            if match in self.urls:
                content = content.replace(match, self.urls[match], 1)
        
        record.getField(self.field).setValue(content)

        return record


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
        print "entra por aqui: " + key        
        return False
