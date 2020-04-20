from storages.backends.s3boto3 import S3Boto3Storage


# Static File Storage Backend
class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


# Public Media File Storage Backend
class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


# Private Media File Storage Backend
class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False