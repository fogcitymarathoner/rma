# -*- coding: utf-8 -*-
"""
helpers.media.utils

Functions for media and image management.

* created: 2013-04-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-11-22 kchan
"""

import os
import re
import datetime
import shutil
import Image
import ExifTags

from garage import get_setting as _s
from garage.logger import logger
from garage.utils import (
    make_dir,
    sha1hash,
    enum,
)
from garage.image_utils import (
    get_image_size,
    resize_image,
    generate_thumb,
    get_file_basename,
    get_img_ext
)
from helpers.crypto.utils import random_key
from helpers.files.utils import create_dir



### defaults

# path to upload images/files to
MEDIA_UPLOAD_PATH = _s('MEDIA_UPLOAD_PATH', 'users')
MEDIA_GROUP_UPLOAD_PATH = _s('MEDIA_GROUP_UPLOAD_PATH', 'groups')
MEDIA_UPLOAD_SUBDIR = _s('MEDIA_UPLOAD_SUBDIR', 'i')
MEDIA_TMP_UPLOAD_PATH = _s('MEDIA_TMP_UPLOAD_PATH', 'tmp')
MEDIA_TMP_UPLOAD_SUBDIR = _s('MEDIA_TMP_UPLOAD_SUBDIR', 'u')
MEDIA_TEST_UPLOAD_PATH = _s('MEDIA_TEST_UPLOAD_PATH', 'testing')

# prefix of url to use for media uploaded to file storage
MEDIA_URL_PREFIX = '%s%s' % (_s('MEDIA_URL'), MEDIA_UPLOAD_PATH)

# name of thumbnail directory
THUMBNAIL_DIRECTORY = _s('THUMBNAIL_DIRECTORY', 'thumbs')

# max image height and width
MAX_IMAGE_HEIGHT = _s('MAX_IMAGE_HEIGHT', 400)
MAX_IMAGE_WIDTH = _s('MAX_IMAGE_WIDTH', 600)

# default image resizing quality
DEFAULT_IMAGE_QUALITY = _s('DEFAULT_IMAGE_QUALITY', 50)

# default thumbnail sizes
DEFAULT_THUMBNAIL_SIZES = _s('DEFAULT_THUMBNAIL_SIZES',
                             (('thumb_square', 100, 100,),
                              ('small', 225, 125,),
                              # ('small', 245, 138,),
                              # ('medium', 500, 280,),
                              # ('large', 600, 338,)
                             ))

# image processing operations (no op, resize or crop)
# * no op -> do not resize or crop
# * resize -> preserve aspect ratio
# * crop -> crop image according to w and h
IMG_OP = enum(NOP=0, RESIZE=1, CROP=2)
DEFAULT_IMG_OP = IMG_OP.NOP

# random key lengh
# * length of random key for generating unique file name
FILENAME_RANDOM_KEY_LEN = _s('FILENAME_RANDOM_KEY_LEN', 128)

# filename components regexp
FILENAME_REGEXP_PAT = r'^([^/]+)(-\d+x\d+)?(\.[^/\.]+)$'
FilenameRegexp = None


### functions to convert path names to urls and vice versa



def is_local_path(path):
    """
    Determine if path is on local file system.
    """
    media_root = _s('MEDIA_ROOT')
    resources_root = _s('RESOURCES_ROOT')
    return path.startswith(media_root) or path.startswith(resources_root)


def local_file_exists(path):
    """
    Verify that path is a file on the local file system.
    """
    return os.path.isfile(path)


def path_to_local_url(path):
    """
    Convert a file system path to relative ``local url path`` for serving media.
    """
    try:
        media_root = _s('MEDIA_ROOT')
        media_url = _s('LOCAL_MEDIA_URL', 'MEDIA_URL')
        return path.replace(media_root, media_url)
    except AttributeError:
        return None


def url_to_local_path(url):
    """
    Convert an url to ``local file path`` for media storage.
    """
    try:
        media_root = _s('MEDIA_ROOT')
        media_url = _s('LOCAL_MEDIA_URL', 'MEDIA_URL')
        return url.replace(media_url, media_root)
    except AttributeError:
        return None


def path_to_url(path):
    """
    Convert a file system path to relative url path for serving media.
    """
    try:
        media_root = _s('MEDIA_ROOT')
        media_url = _s('MEDIA_URL')
        return path.replace(media_root, media_url)
    except AttributeError:
        return None


def url_to_path(url):
    """
    Convert an url to local path for media storage.
    """
    try:
        media_root = _s('MEDIA_ROOT')
        media_url = _s('MEDIA_URL')
        return url.replace(media_url, media_root)
    except AttributeError:
        return None


def get_thumb_dir(image, creat=False):
    """
    Get thumbnail directory for image.
    * default thumbnail directory is a "thumbs" directory inside the
      image directory.
    """
    img_dir = os.path.dirname(image)
    thumbs_dir = THUMBNAIL_DIRECTORY
    path = os.path.join(img_dir, thumbs_dir)
    if creat:
        create_dir(path)
    return path


def get_user_upload_dir(user_id, creat=False):
    """
    Get upload directory for user.
    * the user upload directory is calculate by appending the
      following to MEDIA_ROOT:
    ** MEDIA_UPLOAD_PATH (default: users)
    ** MEDIA_UPLOAD_SUBDIR (default: i)
    ** user id (integer)

    Example path:
    /static/media/users/i/1/image.jpg
    """
    media_root = _s('MEDIA_ROOT')
    path = os.path.join('%s%s' % (media_root, MEDIA_UPLOAD_PATH,),
                        MEDIA_UPLOAD_SUBDIR, str(user_id))
    if creat:
        create_dir(path)
    return path


def get_group_upload_dir(group_id, creat=False):
    """
    Get upload directory for group.
    * the group upload directory is calculate by appending the
      following to MEDIA_ROOT:
    ** MEDIA_GROUP_UPLOAD_PATH (default: groups)
    ** MEDIA_UPLOAD_SUBDIR (default: i)
    ** group id (integer)

    Example path:
    /static/media/groups/i/1/image.jpg
    """
    media_root = _s('MEDIA_ROOT')
    path = os.path.join('%s%s' % (media_root, MEDIA_GROUP_UPLOAD_PATH,),
                        MEDIA_UPLOAD_SUBDIR, str(group_id))
    if creat:
        create_dir(path)
    return path


def get_tmp_upload_dir(creat=False):
    """
    Get temporary storage directory for images.
    * the upload directory is calculate by appending the
      following to MEDIA_ROOT:
    ** MEDIA_TMP_UPLOAD_PATH (tmp)
    ** MEDIA_TMP_UPLOAD_SUBDIR (u)

    Example path:
    /static/media/tmp/u/abcskdakfhdk.jpg
    """
    media_root = _s('MEDIA_ROOT')
    path = os.path.join('%s%s' % (media_root, MEDIA_TMP_UPLOAD_PATH,),
                        MEDIA_TMP_UPLOAD_SUBDIR)
    if creat:
        create_dir(path)
    return path


def get_test_upload_dir(creat=False):
    """
    Get test storage directory for images.
    * the upload directory is calculate by appending the
      following to MEDIA_ROOT:
    ** MEDIA_TEST_UPLOAD_PATH (testing)

    Example path:
    /static/media/tmp/u/abcskdakfhdk.jpg
    """
    media_root = _s('MEDIA_ROOT')
    path = '%s%s' % (media_root, MEDIA_TEST_UPLOAD_PATH,)
    if creat:
        create_dir(path)
    return path


def create_filename(*args, **kwargs):
    """
    Generate filename based on hash of secret key and supplied params.

    Example usage:

        import datatime
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%d.%H%M%S%Z')
        group_id = group_profile.id
        contact_email = group_profile.contact_email
        unique_filename = create_unique_filename(timestamp,
                          group_id, contact_email)

    * if args is empty list function will generate file name using
      timestamp and a random key (of length 'FILENAME_RANDOM_KEY_LEN')

    :param args: list of basestrings to use to construct file name
    :param kwargs: options
    :returns: sha1hashed file name
    """
    # extract options
    append_random_key = kwargs.get('append_random_key', False)
    random_key_len = kwargs.get('random_key_len', FILENAME_RANDOM_KEY_LEN)
    lowercase = kwargs.get('lowercase', False)
    fext = kwargs.get('fext', '')

    # construct parts for hashing
    parts = []

    def _add(x):
        if isinstance(x, (list, tuple)):
            for a in x:
                _add(a)
        else:
            try:
                assert x
                parts.append(str(x))
            except (AssertionError, TypeError):
                pass

    if not args:
        args = [datetime.datetime.utcnow().strftime('%Y%m%d.%H%M%S%Z'),
                random_key(random_key_len)]
    _add(_s('SECRET_KEY'))
    _add(args)
    if append_random_key:
        _add(random_key(random_key_len))
    filename = '%s%s' % (sha1hash('.'.join(parts)), fext)
    if lowercase:
        filename = filename.lower()
    logger().debug('create_filename - parts: %s' % repr(parts))
    logger().debug('create_filename - hashed filename: %s' % filename)
    return filename


def create_unique_filename(*args, **kwargs):
    return create_filename(*args, **kwargs)


def get_image_ext(path, default_ext=None, use_path_ext=False):
    """
    Return file name and extension for image.
    * if there's something wrong with the image, use the file name's
      extension as a replacement.

    :param path: image path
    :param default_ext: default extension if PIL can't determine image type
    :param use_path_ext: if True, get extension from file name
    :returns: file extension
    """
    try:
        fext = get_img_ext(path, default_ext=None)
        assert fext
    except AssertionError:
        if use_path_ext:
            fname, fext = os.path.splitext(path)
        else:
            fext = default_ext
    return fext


### image upload helper function

def save_uploaded_file(uploaded_file, dst_dir, filename):
    """
    Save uploaded file (from form submission) to destination.
    * create destination directory if it does not exist.
    * FIXME: raise error if save fails

    :returns: path to saved image
    """
    create_dir(dst_dir)
    dst_path = os.path.join(dst_dir, filename)
    with open(dst_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return dst_path


### delete images


# def delete_images(entry, image_fields):
#     """
#     Delete image associated with entry and all its thumbnails.
#     * use ``helpers.files.utils.delete_images`` to proccess local and
#       remote storage deletions.
#     """
#     from helpers.files.utils import delete_images as storage_delete
#     return storage_delete(entry, image_fields)


def delete_images(entry, image_fields=None):
    """
    Delete image associated with entry and all its thumbnails.
    * if image_fields is None, check entry for get_image_fields
      method.

    Example usage:

    ENTRY_IMAGES = (
        'image',
        'thumbnail',
        'thumbnail_small'
    )
    delete_images(entry, ENTRY_IMAGES)

    * FIXME: add get_images method to model to fetch image paths
      directly instead of using field to fetch paths

    :param entry: object instance
    :param image_fields: list of field names for thumbnails
    :returns: number of errors encountered (0 is successful)
    """
    from helpers.files.utils import delete_remote_media

    use_remote_storage = _s('USE_REMOTE_STORAGE', False)
    errors = 0

    def _delete(url):
        e = 0
        if use_remote_storage:
            if not is_local_path(url):
                ok = delete_remote_media(url)
                if not ok:
                    e += 1
                logger().debug('deleted remote image - %s %s' % (ok, url))
        path = url_to_path(url)
        if os.path.isfile(path):
            os.remove(path)
            ok = os.path.isfile(path) == False
            if not ok:
                e += 1
            logger().debug('deleted image - %s %s' % (ok, path))
        return e

    if entry:
        if image_fields is None:
            if hasattr(entry, 'get_image_fields'):
                image_fields = entry.get_image_fields()
        if isinstance(image_fields, (list, tuple)):
            for img in image_fields:
                try:
                    assert img
                    url = getattr(entry, img)
                    assert url
                except AssertionError:
                    pass
                else:
                    result = _delete(url)
                    errors += result
                    setattr(entry, img, None)

    logger().debug('delete_images - errors: %d' % errors)
    return errors


### image processing helpers

def resize_original_image(img_path,
                          max_width=0,
                          max_height=0,
                          quality=DEFAULT_IMAGE_QUALITY,
                          op=DEFAULT_IMG_OP,
                          addwh=False,
                          dup=False):
    """
    resize image to below max width or max height.
    * NOTE: uses local file system for copies and storage.
    * set max_width to 0 or max_height to 0 to disable resizing width or height.
    * resizes to RGB color space.
    * set ``addwd`` to append image dimensions (width x height) filename.
    * set ``dup`` to True to make copy of image before resizing.

    :param img_path: local file system path to image
    :param max_width: set maximum width of image (for resizing)
    :param max_height: set maximum height of image (for resizing)
    :param quality: compression quality (0 to 100)
    :param op: operation to perform (IMG_OP.RESIZE or IMG_OP.CROP)
    :param addwh: add image dimension (width x height) to file name
    :param dup: if True, make copy of image before working on it.
    :returns: path of processed image
    """
    transform = False
    if op == IMG_OP.RESIZE:
        crop = False
        w, h = get_image_size(img_path)
        if max_width > 0 and w > max_width:
            ratio = (1.0 * w) / h
            w = max_width
            h = int((1.0 * w) / ratio)
            transform = True
        elif max_height > 0 and h > max_height:
            ratio = (1.0 * w) / h
            h = max_height
            w = int(ratio * h)
            transform = True
    elif op == IMG_OP.CROP:
        w = max_width
        h = max_height
        crop = transform = True

    if transform:
        # resize image
        dst_dir = os.path.dirname(img_path)
        fbase = get_file_basename(img_path)
        fext = get_image_ext(img_path, use_path_ext=True)
        img = resize_image(Image.open(img_path), (w, h,), crop)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        w, h = img.size
        filename = '%s-%dx%d.%s' % (fbase, w, h, fext)
        output = os.path.join(dst_dir, filename)
        img.save(output, quality=quality)
        if not dup:
            shutil.move(output, img_path)
        else:
            img_path = output
    elif addwh:
        # image does not need resizing but we need to append wxh to
        # file name and optionally (if dup is True) make a copy.
        dst_dir = os.path.dirname(img_path)
        fbase = get_file_basename(img_path)
        fext = get_image_ext(img_path, use_path_ext=True)
        w, h = get_image_size(img_path)
        filename = '%s-%dx%d.%s' % (fbase, w, h, fext)
        output = os.path.join(dst_dir, filename)
        if dup:
            shutil.copyfile(img_path, output)
        else:
            shutil.move(img_path, output)
        img_path = output

    return img_path


def fix_image_rotation(img_path):
    """
    Fix image rotation.
    * see: http://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image

    """
    try:
        image = Image.open(img_path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        if hasattr(image, '_getexif'): # only present in JPEGs
            e = image._getexif()       # returns None if no EXIF data
            if e is not None:
                exif = dict(e.items())
                orientation = exif[orientation]
                if orientation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    image = image.transpose(Image.ROTATE_90)
                image.save(img_path)
    except:
        # traceback.print_exc()
        pass
    return img_path


def create_thumbs(image, dst_dir, thumb_sizes, quality=DEFAULT_IMAGE_QUALITY):
    """
    Create thumbnails from image and saves them to destination directory.
    * this function uses garage.img_utils to generate thumbnails on the
      local file system -- i.e. does not save to remote storage.

    THUMBNAIL_SIZES = (
    ('thumb_square', 100, 100,),
    ('thumb_nano',    24,  24,),
    ('thumb_micro',   48,  48,),
    # ('small', 225, 125,),
    # ('small', 245, 138,),
    # ('medium', 500, 280,),
    # ('large', 600, 338,)
    )

    :param image: path to original image
    :param dst_dir: path to thumbnail directory
    :param thumb_sizes: list of thumbnail sizes (tuple of name, width, height)
    :param quality: 0-100
    :returns: dict of { name: path } for each thumbnail size
    """
    thumbs = {}
    try:
        assert image
        make_dir(dst_dir)
        for i in thumb_sizes:
            try:
                name, width, height = i
                path = generate_thumb(image, width, height,
                                      quality, dst_dir)
                thumbs[name] = path
            except:
                # FIXME: handle error with some kind of fallback
                pass
    except AssertionError:
        pass
    return thumbs


def extract_fname_parts(filename):
    """
    Helper function to extract media file name componets.
    * filename should be in the form: abcdef-100x100.jpg
    * function will extract the following:
    ** fbase - corresponds to file base name without width/height or
       suffix (e.g. abcdef)
    ** fwh - corresonds to width x height string component
       (e.g. 100x100)
    ** fext - corresponds to file extension (e.g. .jpg)

    :param filename: media file name
    :returns: tuple of (fbase, fwh, fext) or ('', '', '') it no match.
    """
    global FilenameRegexp
    if FilenameRegexp is None:
        FilenameRegexp = re.compile(FILENAME_REGEXP_PAT, re.I)
    m = FilenameRegexp.match(filename)
    if m:
        matched = m.groups()
    else:
        matched = ('', '', '')
    return matched


def copy_media_to_remote(path, verify=True):
    """
    Verify local file path has remote version and copy to remote
    storage if remote does not exist.
    * if verify is True, function will skip copy if remote version
      exists.
    * NOTE: this is for files in the ``media`` directory.

    :param path: local file path
    :param verify: if True, verify and skip copy if remote exists
    :returns: remote server media url or None if error
    """
    from helpers.files.utils import (
        local_path_to_remote_media_url,
        remote_media_url_exists,
        save_to_remote_media_storage,
    )
    try:
        assert local_file_exists(path)
    except AssertionError:
        url = None
        logger().debug(
            'copy_media_to_remote - local file not found -'
            'local: %s' % path)
    else:
        copy_to_remote = True
        if verify:
            url = local_path_to_remote_media_url(path)
            remote_exists = remote_media_url_exists(url)
            if remote_exists:
                copy_to_remote = False
                logger().debug(
                    'copy_media_to_remote - remote exists - '
                    'local: %s / remote: %s' %
                    (path, url))
        if copy_to_remote:
            url = save_to_remote_media_storage(path)
            logger().debug(
                'copy_media_to_remote - copied to remote - '
                'local: %s / remote: %s' %
                (path, url))
    return url
