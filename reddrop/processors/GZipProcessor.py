import gzip

from .BaseProcessor import BaseProcessor

class GZipProcessor(BaseProcessor):
    name = "gzip"
    
    def processData(self, encoded:bytes, *args, **kwargs):
        return gzip.decompress(encoded)

    def validate(self, encoded:bytes):
        return encoded[:2] == bytes([0x1f,0x8b])