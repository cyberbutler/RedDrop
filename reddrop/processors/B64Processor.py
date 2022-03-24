import re
import base64

from .BaseProcessor import BaseProcessor

class B64Processor(BaseProcessor):
    name = "b64"
    priority = 0
    regex = re.compile(
            b'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
    
    def processData(self, encoded:bytes, *args, **kwargs):
        # We replace any space characters with + symbols as clients, proxies, 
        # and servers may interpret base64 + symbols as spaces before reaching this handler
        encoded = encoded.replace(b' ', b'+')
        encoded = encoded.replace(b'\n', b'') # Remove new line characters
        decoded = base64.b64decode(encoded)
        return decoded
   
    def validate(self, encoded:bytes):
        """
        Detecting base64 without any contextual information can be pretty tricky, and this is about the best we can do. If you run into issues, bypass this method.
        """
        encoded = encoded.replace(b' ', b'+') # Convert spaces to + characters
        encoded = encoded.replace(b'\n', b'') # Remove new line characters
        
        return bool(self.regex.match(encoded))
