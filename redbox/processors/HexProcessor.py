import re
import codecs
from .BaseProcessor import BaseProcessor

class HexProcessor(BaseProcessor):
    name = "hex"
    priority = 10    
    
    def processData(self, encoded:bytes, *args, **kwargs):
        encoded = encoded.replace(b'\n', b'')
        return codecs.decode(encoded, 'hex')

    def validate(self, encoded:bytes):
        encoded = encoded.replace(b'\n', b'')
        regex = re.compile(b'([0-9a-f]{2,})|([0-9A-F]{2,})')
        return bool(regex.match(encoded)) and len(encoded) % 2 == 0