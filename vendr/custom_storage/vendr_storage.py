from django.core.files.storage import FileSystemStorage

from .aws import S3Adapter


class VendrMediaStorage(FileSystemStorage):

    def __init__(self):
        
        self.location = 'media.vendr'
        self.storage  = S3Adapter(self.location)

    def get_available_name(self, name, max_length=None):

        if self.exists(name):
            raise ValueError('error: a file with this name already exists.')

        return name

    def _open(name, mode='rb'):

        print 'OPEN'
            

    def _save(self, name, content):

        # Save the file with the given name to the base location.
        name = self.storage.save(name, content)
        return name

    def delete(self, name):

        print 'dELETE'
        lkjsd;

