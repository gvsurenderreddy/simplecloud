# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from simplecloud.user import User
from simplecloud.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

    def test_show(self):
        self._test_get_request('/', 'frontend/login.html')

    def test_login(self):
        self._test_get_request('/login', 'frontend/login.html')

    def test_logout(self):
        self.login('demo', '123456')
        self._logout()

class TestUser(TestCase):

    def test_home(self):
        response = self.client.get('/user/')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/', safe=''))

        self.login('demo', '123456')
        self._test_get_request('/vms/', 'vm/index.html')

class TestSettings(TestCase):

    def test_profile(self):
        endpoint = '/settings/profile'

        response = self.client.get(endpoint)
        self.assertRedirects(response, location='/login?next=%s' % url_quote(endpoint, safe=''))

        self.login('demo', '123456')
        response = self.client.get('/settings/profile')
        self.assert200(response)
        self.assertTemplateUsed("settings/profile.html")

    def test_password(self):
        endpoint = '/settings/password'

        response = self.client.get(endpoint)
        self.assertRedirects(response, location='/login?next=%s' % url_quote(endpoint, safe=''))

        self.login('demo', '123456')
        response = self.client.get('/settings/password')
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        data = {
            'password': '123456',
            'new_password': '654321',
            'password_again': '654321',
        }
        response = self.client.post(endpoint, data=data)
        assert "help-block error" not in response.data
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        updated_user = User.query.filter_by(name='demo').first()
        assert updated_user is not None
        assert updated_user.check_password('654321')


class TestError(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')


class TestAdmin(TestCase):

    def test_index(self):
        self.client.get('/admin/', follow_redirects=True)
        self.assertTemplateUsed('frontend/login.html')

        response = self.login('admin', '123456')
        self.assert200(response)

        response = self.client.get('/admin/')
        self.assertTemplateUsed('admin/index.html')
