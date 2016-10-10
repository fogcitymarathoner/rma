# -*- coding: utf-8 -*-
"""
helpers.workflow.tests.

Tests for helpers.workflow module.

* created: 2013-10-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-17 kchan
"""
import re
import string

from django.core.urlresolvers import reverse
from garage import get_setting as _s
from testing import (
    ProfileUserTestCase,
)
