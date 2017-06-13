import boto3

class S3Adapter(object):

    def __init__(self, location):
        
        self.location = location
        
        self.resource = 's3'
        self.s3 = boto3.resource(self.resource)
        
    def save(self, name, content):
        
        bucket_name = self.location
        bucket = self.s3.Bucket(bucket_name)
        
        response = bucket.put_object(Key=name, Body=content)
        
        name = self._format_name(bucket=response._bucket_name, key=response._key)
        return name

    def _format_name(self, bucket, key):

        BASE = 'https://s3.ca-central-1.amazonaws.com/'
        name = '{}{}/{}'.format(BASE, bucket, key)
        
        return name

