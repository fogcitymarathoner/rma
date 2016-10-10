# -*- coding: utf-8 -*-
"""
helpers.files.storage

Storage backend for remote media servers.

* created: 2013-08-12 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-08-13 kchan
"""

from storages.backends.s3boto import S3BotoStorage

from .settings import (
    MEDIA_STORAGE_PREFIX,
    RESOURCES_STORAGE_PREFIX,
)


class ResourcesStorage(S3BotoStorage):
    """
    Storage class to allow s3 storage with location/folder prefix.

    Borrowed from:
    http://tartarus.org/james/diary/2013/07/18/fun-with-django-storage-backends
    """
    def __init__(self, *args, **kwargs):
        kwargs['location'] = RESOURCES_STORAGE_PREFIX
        return super(ResourcesStorage, self).__init__(*args, **kwargs)


class MediaStorage(S3BotoStorage):
    """
    Storage class to allow s3 storage with location/folder prefix.

    Borrowed from:
    http://tartarus.org/james/diary/2013/07/18/fun-with-django-storage-backends
    """
    def __init__(self, *args, **kwargs):
        kwargs['location'] = MEDIA_STORAGE_PREFIX
        return super(MediaStorage, self).__init__(*args, **kwargs)


resources_storage = ResourcesStorage()
media_storage = MediaStorage()
