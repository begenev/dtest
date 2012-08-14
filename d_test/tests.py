"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse

from django.test import TestCase


class MainTest(TestCase):

    fixtures = ['data.json']

    def test_ajax_edit(self):
        edit_url = reverse('cell_ajax_edit')
        response = self.client.post(edit_url, data={
            'value':'2012-08-15',
            'id':'cell_0_3_date'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(edit_url, data={
            'value':'2012-15',
            'id':'cell_0_3_date'
        }, follow=True)

        self.assertEqual(response.status_code, 404)

        response = self.client.post(edit_url, data={
            'value':'abc',
            'id':'cell_0_2_int'
        }, follow=True)

        self.assertEqual(response.status_code, 404)

        response = self.client.post(edit_url, data={
            'value':'15',
            'id':'cell_0_2_int'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(edit_url, data={
            'value':'Jhon',
            'id':'cell_0_1_char'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
