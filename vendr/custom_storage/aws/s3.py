import boto3

class S3Adapter(object):

    def __init__(self, location):
        
        self.location = location
        
        self.resource = 's3'
        self.extension = 'png'
        self.s3 = boto3.resource(self.resource)
        
    """ Save the file to our s3 bucket.
        Args:
            name (str) -- The generated key for our file.
            content (file) -- The actual file we're uploading.
    """
    def save(self, name, content):
        
        bucket_name = self.location
        bucket = self.s3.Bucket(bucket_name)
        
        name = '{}.{}'.format(name, self.extension)
        response = bucket.put_object(Key=name, Body=content)

        name = self._format_name(bucket=response._bucket_name,
                key=response._key)

        return name

    """ S3 is returning only parts of the resource URL, so if we
        want the full URL for our Image's `name` field then we'll
        have to reconstruct / format the parts ourselves.
        Args:
            bucket (str) -- The s3 bucket name.
            key (str) -- The key of the file we just uploaded.
    """
    def _format_name(self, bucket, key):

        BASE = 'https://s3.ca-central-1.amazonaws.com/'
        name = '{}{}/{}'.format(BASE, bucket, key)
        
        return name

