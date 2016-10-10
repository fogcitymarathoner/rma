# -*- coding: utf-8 -*-
"""
helpers.files.utils

Utility functions for using storage backends.

* created: 2013-08-12 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-26 kchan
"""

import os

from django.core.files.storage import default_storage
from django.core.files import File
from garage import get_setting as _s
from garage.image_utils import get_img_ext
from garage.logger import logger

from .storage import (
    resources_storage,
    media_storage,
)
from .settings import (
    RESOURCES_ROOT,
    RESOURCES_URL,
    MEDIA_ROOT,
    MEDIA_URL,
    FILE_IO_CHUNK_SIZE,
    UNKNOWN_MIME_TYPE,
    MIME_TYPES,
    MEDIA_STORAGE_PREFIX,
    RESOURCES_STORAGE_PREFIX,
)



def local_to_remote_media_path(path):
    """
    Get remote path corresponding to local file path.
    * for S3 storage the remote path is the bucket key.

    :param path: local file path
    :returns: remote path corresponding to local file
    """
    prefix = '%s/' % MEDIA_STORAGE_PREFIX
    return path.replace(MEDIA_ROOT, prefix)


def local_path_to_remote_media_url(path):
    """
    Return the url of the remote version corresponding to local file.
    :param path: local file path
    :returns: remote url corresponding to local file
    """
    remote_path = path.replace(MEDIA_ROOT, '')
    return '%s%s' % (MEDIA_URL, remote_path)


def remote_media_exists(remote_path):
    """
    Verify that the remote version of the local file exists.

    :param remote_path: remote path of file
    :returns: True if remote file exists else False
    """
    return media_storage.exists(remote_path)


def remote_media_url_exists(url):
    """
    Verify that the remote version of the local file exists.

    :param url: url of remote file
    :returns: True if remote file exists else False
    """
    return remote_media_exists(url.replace(MEDIA_URL, ''))


def local_to_remote_resource_path(path):
    """
    Get remote path corresponding to local file path.
    * for S3 storage the remote path is the bucket key.
    * NOTE: this is for static files in the ``resources`` directory.

    :param path: local file path
    :returns: remote path corresponding to local file
    """
    prefix = '%s/' % RESOURCES_STORAGE_PREFIX
    return path.replace(RESOURCES_ROOT, prefix)


def local_path_to_remote_resource_url(path):
    """
    Return the url of the remote version corresponding to local file.
    * NOTE: this is for static files in the ``resources`` directory.

    :param path: local file path
    :returns: remote url corresponding to local file
    """
    remote_path = path.replace(RESOURCES_ROOT, '')
    return '%s%s' % (RESOURCES_URL, remote_path)


def remote_resource_exists(remote_path):
    """
    Verify that the remote version of the local file exists.
    * NOTE: this is for static files in the ``resources`` directory.

    :param remote_path: remote path of file
    :returns: True if remote file exists else False
    """
    return resources_storage.exists(remote_path)


def remote_resource_url_exists(url):
    """
    Verify that the remote version of the local file exists.
    * NOTE: this is for static files in the ``resources`` directory.

    :param url: url of remote file
    :returns: True if remote file exists else False
    """
    return remote_resource_exists(url.replace(RESOURCES_URL, ''))


def save_to_remote_storage(path, storage=None):
    """
    Push a local file to remote media storage.

    :param path: local path of file
    :param storage: storage instance to use (default: default_storage)
    :returns: url of file on remote storage server
    """
    if not path or not os.path.isfile(path):
        logger().debug('save to remote storage - cannot find file: %s' % path)
        remote_path = path
    else:
        if not storage:
            storage = default_storage

        if storage == resources_storage:
            fkey = path.replace(RESOURCES_ROOT, '')
        else:
            fkey = path.replace(MEDIA_ROOT, '')

        # determine mime type
        fext = get_img_ext(path)
        content_type = MIME_TYPES.get(fext, UNKNOWN_MIME_TYPE)

        # write file to remote server
        file = storage.open(fkey, 'w')
        storage.headers.update({"Content-Type": content_type})
        f = open(path, 'rb')
        media = File(f)
        for chunk in media.chunks(chunk_size=FILE_IO_CHUNK_SIZE):
            file.write(chunk)
        file.close()
        media.close()
        f.close()

        # construct remote url
        if storage == resources_storage:
            remote_path = '%s%s' % (RESOURCES_URL, fkey)
        else:
            remote_path = '%s%s' % (MEDIA_URL, fkey)
        logger().debug(
            'save_to_remote_storage - local: %s / remote: %s / mime-type: %s'
            % (path, remote_path, content_type))

    return remote_path


def save_to_remote_resources_storage(path):
    """
    Push file to remote resources storage.

    :param path: local path of file
    :returns: url of file on remote storage server
    """
    return save_to_remote_storage(path, storage=resources_storage)


def save_to_remote_media_storage(path):
    """
    Push file to remote media storage.

    :param path: local path of file
    :returns: url of file on remote storage server
    """
    return save_to_remote_storage(path, storage=media_storage)


def delete_remote_resource(url):
    """
    Delete file on remote storage.

    :param url: url of file
    :returns: True if remote file no longer exists else False
    """
    storage = resources_storage
    fkey = url.replace(RESOURCES_URL, '')
    if storage.exists(fkey):
        storage.delete(fkey)
    return storage.exists(fkey) == False


def delete_remote_media(url):
    """
    Delete file on remote storage.

    :param url: url of file
    :returns: True if remote file no longer exists else False
    """
    storage = media_storage
    fkey = url.replace(MEDIA_URL, '')
    if storage.exists(fkey):
        storage.delete(fkey)
    return storage.exists(fkey) == False


def delete_images(entry, image_fields):
    """
    Delete image associated with entry and all its thumbnails.
    * use ``helpers.media.utils.delete_images`` to proccess local and
      remote storage deletions.
    """
    from helpers.media.utils import delete_images as _delete
    return _delete(entry, image_fields)


def create_dir(path):
    """
    Utility function to create directory on local file system.

    :param path: absolute path to directory
    :returns: path or None if directory does not exist
    """
    if not os.path.isdir(path):
        os.makedirs(path)
        if not os.path.isdir(path):
            path = None
    return path


def save_local_file(uploaded_file, path, fperms='wb+',
                    chunk_size=FILE_IO_CHUNK_SIZE):
    """
    Save file upload to local file system.
    """
    with open(path, fperms) as destination:
        for chunk in uploaded_file.chunks(chunk_size=chunk_size):
            destination.write(chunk)
    return path


def delete_local_file(path):
    """
    Delete local file.

    :param path: path to local file
    :returns: True if file no longer exists
    """
    if os.path.isfile(path):
        os.remove(path)
    return os.path.isfile(path) == False
