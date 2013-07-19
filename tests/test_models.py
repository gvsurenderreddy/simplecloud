# -*- coding: utf-8 -*-

from simplecloud.user import User

from tests import TestCase


class TestUser(TestCase):

    def test_count(self):

        assert User.query.count() == 2
