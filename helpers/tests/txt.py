# -*- coding: utf-8 -*-
"""
helpers.tests.txt

Tests for helpers.txt module.

* created: 2013-10-27 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

import re
import sys
from cStringIO import StringIO

from helpers.test.base import SimpleTestCase
from helpers.test.utils import module_exists

from helpers.txt.utils import (
    uprint,
    tidy_msg,
    html_to_text,
)


# strings for testing tidy_msg function

DUMMY_TEXT = u"""\
one


two


three


"""

FORMATTED = u"""\
one

two

three
"""

HTML_MSG = u"""\
<html>
    <head>
        <title>Test Email</title>
    </head>
    <body>
        <div style="max-width: 720px; padding: 20px">
            <p>Hello! This is a test email message.</p>
            <p>-- admin@example.com</p>
        </div>
    </body>
</html>
"""

TXT_MSG = u"""\
Test Email

Hello! This is a test email message.

-- admin@example.com
"""


# test cases

class TxtTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = [
            'helpers.txt',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))

    def test_uprint(self):
        """
        Ensure uprint function is displaying unicode text correctly.
        """
        self._msg('test', 'test_uprint', first=True)
        s = u''
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        uprint(s)
        output = mystdout.getvalue().decode('utf-8')
        sys.stdout = old_stdout
        # output contains newline so we add newline to the string to
        # make them both end in newlines.
        txt = u'%s\n' % s
        self.assertEqual(txt, unicode(output))
        self._msg('original', s)
        self._msg('result', output)

    def test_tidy_msg(self):
        """
        Ensure tidy_msg function is formatting text correctly.
        """
        self._msg('test', 'test_tidy_msg', first=True)
        raw_text = DUMMY_TEXT
        result = tidy_msg(raw_text)
        self.assertEqual(result, FORMATTED)
        self._msg('raw text', repr(raw_text), linebreak=True)
        self._msg('result', repr(result), linebreak=True)

    def test_html_to_text(self):
        """
        Ensure html_to_text function is formatting text correctly.
        """
        self._msg('test', 'html_to_text', first=True)
        html = HTML_MSG
        txt = TXT_MSG
        result = html_to_text(html)
        self.assertEqual(result, txt)
        self._msg('html', html, linebreak=True)
        self._msg('txt', txt, linebreak=True)
        self._msg('result', result, linebreak=True)
