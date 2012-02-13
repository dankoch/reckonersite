'''
Created on Jan 26, 2012

@author: danko
Upload handlers used throughout The Reckoner.
'''
from django.core.files.uploadhandler import FileUploadHandler, StopUpload

class ReckoningImageUploadHandler(FileUploadHandler):
    """
    This upload handler inspects incoming Reckoning images to ensure they're the right size.
    If they're not, then they stop and raise an exception.
    """

    QUOTA = 250 * 2**10 # 300 KB

    def __init__(self, request=None):
        super(ReckoningImageUploadHandler, self).__init__(request)
        self.total_upload = 0

    def receive_data_chunk(self, raw_data, start):
        self.total_upload += len(raw_data)
        if self.total_upload >= self.QUOTA:
            raise FileTooBigException(True)
        return raw_data
    
    def new_file(self, field_name, file_name, content_type, content_length, charset):
        if (content_length >= self.QUOTA):
            raise FileTooBigException(True)
        return None

    def file_complete(self, file_size):
        return None
    
class FileTooBigException(StopUpload):

    def __init__(self, connection_reset=True):    
        super(FileTooBigException, self).__init__(connection_reset=connection_reset)