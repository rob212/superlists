from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest


class HomePageTest(TestCase):
    def test_rootURL_resolvesToHomePageView(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_homePageReturnsCorrectHtml(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
