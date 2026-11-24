from .local import LocalBlobStore
from .s3 import S3BlobStore

def create_blobstore(settings):

    if settings.STORAGE_BACKEND == "local":
        return LocalBlobStore(settings.BLOBSTORE_ROOT)

    if settings.STORAGE_BACKEND == "s3":
        return S3BlobStore(settings.S3_BUCKET)

    raise ValueError("Unsupported storage backend")