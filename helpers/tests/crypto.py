# -*- coding: utf-8 -*-
"""
helpers.tests.crypto

Tests for helpers.crypto module.

* created: 2013-09-01 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""
import re
import string

from django.core.urlresolvers import reverse

from helpers.test.base import SimpleTestCase
from helpers.test.utils import module_exists
from helpers.crypto.utils import (
    random_key,
    random_ndigits,
    ezencode,
    ezdecode,
)


class CryptoTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = [
            'helpers',
            'helpers.crypto',
            'helpers.crypto.utils',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))

    def test_random_key(self):
        """
        Test random_key function.
        """
        self._msg('test', 'random_key', first=True)
        """
        for key_len in (1, 2, 3, 8, 16, 72, 127, 99, 512, 1024, 9999):
            rkey = random_key(key_len)
            self.assertEqual(len(rkey), key_len)
            self._msg(key_len, rkey)

            # test chararter sets 1
            charset = 'a'
            rkey = random_key(key_len, charset=charset)
            ch = string.ascii_letters
            for c in rkey:
                self.assertTrue(c in ch)
            # test character sets 2
            charset = 'n'
            rkey = random_key(key_len, charset=charset)
            ch = string.digits
            for c in rkey:
                self.assertTrue(c in ch)
            # test character sets 3
            charset = 'an'
            rkey = random_key(key_len, charset=charset)
            ch = string.ascii_letters + string.digits
            for c in rkey:
                self.assertTrue(c in ch)
            # test character sets 4
            charset = 'anp'
            rkey = random_key(key_len, charset=charset)
            ch = string.ascii_letters + string.digits + string.punctuation
            for c in rkey:
                self.assertTrue(c in ch)
        """

    def test_random_ndigits(self):
        """
        Test random_ndigits function.
        """
        self._msg('test', 'random_ndigits', first=True)
        """
        for key_len in range(1, 17):
            n = random_ndigits(key_len)
            self.assertEqual(len(str(n)), key_len)
            self._msg('ndigits: %d' % key_len, n)
        """
    def test_ezencode_ezdecode_1(self):
        """
        Test ezencode and ezdecode functions.
        """
        self._msg('test', 'exencode and ezdecode', first=True)
        plaintext = "Attack at dawn"
        ciphertext = ezencode(plaintext)
        decrypted = ezdecode(ciphertext)
        self.assertEqual(plaintext, decrypted)
        self._msg('plaintext', plaintext)
        self._msg('ciphertext', ciphertext)
        self._msg('decrypted', decrypted)

    def test_ezencode_ezdecode_2(self):
        """
        Test ezencode and ezdecode functions.
        """
        self._msg('test', 'ezencode and ezdecode', first=True)
        for encoding in ('base16', 'base32', 'base64', None):
            plaintext = "Attack at dawn"
            ciphertext = ezencode(plaintext, encoding=encoding)
            decrypted = ezdecode(ciphertext, encoding=encoding)
            self.assertEqual(plaintext, decrypted)
            self._msg('encoding', encoding)
            self._msg('plaintext', plaintext)
            self._msg('ciphertext', ciphertext, linebreak=True)
            self._msg('decrypted', decrypted)
