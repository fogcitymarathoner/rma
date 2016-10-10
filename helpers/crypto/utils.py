# -*- coding: utf-8 -*-
"""
helpers.crypto.utils

Encrypt/descrypt utility functions.

* created: 2013-01-24 kevin chan <kefin@makedostudio.com>
* updated: 2013-09-01 kchan
"""

import os
import datetime
import random
import string

from minipylib.crypto import (
    encode_data,
    decode_data,
    gen_secret_key,
    DEFAULT_KEY_CHAR_SET,
)
from garage import get_setting as _s



# encode/decode utility functions

def ezencode(data, secret_key=None, encoding='base16'):
    """
    Encrypt data and encode in base16 or some other format.
    """
    if not secret_key:
        secret_key = _s('SECRET_KEY')
    return encode_data(data, secret_key, pickle_data=True, encoding=encoding)


def ezdecode(encrypted, secret_key=None, encoding='base16'):
    """
    Decode and decrypt data previously encoded using my_encode_data.
    """
    if not secret_key:
        secret_key = _s('SECRET_KEY')
    return decode_data(encrypted, secret_key, pickle_data=True, encoding=encoding)


# utility functions for packing/unpacking cookies

def encode_cookie(data, max_age, magic=None, secret_key=None):
    """
    Prep and encode session cookie

    * this is a utility function to prepare a cookie

    Cookie contains the following keys:

    * max_age - max age of cookie before expiration
    * expiration - expiration time
    * expiration_timestamp - expiration timestamp in iso8601 format
    * cookie_timestamp - timestamp of cookie in iso-8601 format
    * magic - magic code for authenticaton when decoding

    :param secret_key: secret key used for encryption/decryption
    :returns: encrypted string containing cookie data
    """
    if magic is None:
        magic = ''
    expire_cookie = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    #expiration_timestamp = expire_cookie.strftime("%a, %d %b %Y %H:%M:%S GMT")
    expiration_timestamp = expire_cookie.strftime("%Y-%m-%dT%H:%M:%S")
    cookie_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    cookie_data = {
        'max_age': max_age,
        'expiration': expire_cookie.isoformat(),
        'expiration_timestamp': expiration_timestamp,
        'cookie_timestamp': cookie_timestamp,
        'magic': magic,
        'data': data
    }
    return ezencode(cookie_data, secret_key=secret_key)


def decode_cookie(cookie, secret_key=None):
    """
    Decode cookie encoded using above function

    :param cookie: encoded cookie data string
    :param secret_key: secret key used for encryption/decryption
    :returns: decoded cookie data
    """
    return ezdecode(cookie, secret_key=secret_key)


def random_key(length, charset=DEFAULT_KEY_CHAR_SET, key_string=None):
    """
    Returns a random alphanumeric string of length 'length'
    * see minipylib.crypto.gen_secret_key

    :param length: length of key to generate
    :param charset: character sets to use (a, l, u, n, p)
    :param key_string: use provided string for key characters
    :returns: random string
    """
    return gen_secret_key(keysize=length,
                          charset=charset,
                          key_string=key_string)


# OlD VERSION
# def random_ndigits(n):
#     """
#     Return a string consisting of n digits.
#     * from: http://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
#     * NOTE: this is not secure -- do not use for secure data.
#     * ``n`` should probably be a small value (less than the max size
#       of an int (32 bits))
#
#     :param n: number of digits to generate random number for
#     :returns: an integer of n digits
#     """
#     range_start = 10**(n-1)
#     range_end = (10**n)-1
#     return random.randint(range_start, range_end)


def random_ndigits(n):
    """
    Return a string consisting of n digits.

    :param n: number of digits to generate random number for
    :returns: a string of n digits
    """
    return random_key(n, charset='n')


def decode_form_data(data, key, default=None):
    """
    Retrieve encoded _extra_data from form's cleaned data.

    Example usage:

        extra_data = decode_data(data, '_extra_data')
        try:
            entry_id = int(extra_data.get('id'))
        except (AttributeError, TypeError):
            pass

    :param data: cleaned data returned by form
    :param key: name of key to in data
    :param default: default value to return if decode fails
    :returns: decoded info corresponding to key
    """
    try:
        _data = data.get(key)
        assert _data
        decoded = ezdecode(_data)
    except (AssertionError, AttributeError):
        decoded = default
    return decoded
