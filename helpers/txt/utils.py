# -*- coding: utf-8 -*-
"""
helpers.txt.utils

Utility functions for helpers.txt module.

* created: 2013-10-27 kevin chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

import re

from django.utils.html import strip_tags


default_encoding = "utf-8"

def uprint(data, encoding=default_encoding):
    """
    Print unicode output to stdout.

    :param data: data to print.
    :param encoding: data encoding (default is `utf-8`).
    """
    print data.encode(encoding)


def tidy_msg(msg):
    """
    Utility function to tidy up text message by compressing multiple
    blank lines.
    * multiple (>2) blank lines are reduced to 2.

    :param msg: text message
    :returns: tidied up message with multiple blank lines removed.
    """
    if isinstance(msg, (basestring, unicode)):
        lines = unicode(msg).split(u'\n')
        s = []
        run = 0
        for line in lines:
            txt = line.strip()
            if len(txt) == 0:
                if run < 1:
                    s.append(u'')
                run += 1
            else:
                run = 0
                s.append(txt)
        msg = u'\n'.join(s)
    return msg


def html_to_text(html):
    """
    Simple function to convert html content to text.
    * uses Django strip_tags function to convert html to text;
    * multiple blank lines are reduced to 2;
    * strips beginning and ending white space.

    :param html: html content
    :returns: plain text content after conversion
    """
    txt = tidy_msg(strip_tags(html))
    lines = []
    for line in txt.splitlines():
        s = line.strip()
        if len(s) > 0:
            lines.append(s)
    txt = u'\n\n'.join(lines)
    txt = u'%s\n' % txt
    return txt
