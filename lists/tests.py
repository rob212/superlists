import re
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest


class HomePageTest(TestCase):
    def test_rootURL_resolvesToHomePageView(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        # remove CSRF token to allow us to test
        observed_html = self.remove_csrf_from_markup(response)

        self.assertIn(expected_html, observed_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        expected_entry = 'A new list item'
        request.POST['item_text'] = expected_entry

        response = home_page(request)

        self.assertIn(expected_entry, response.content.decode())
        expected_html = render_to_string('home.html', {'new_item_text': expected_entry})

        # remove CSRF token to allow us to test
        observed_html = self.remove_csrf_from_markup(response)

        self.assertEqual(expected_html, observed_html)

    def remove_csrf_from_markup(self, response):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        observed_html = re.sub(csrf_regex, '', response.content.decode())
        return observed_html
