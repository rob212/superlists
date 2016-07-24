import re
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item


class HomePageTest(TestCase):
    def setUp(self):
        self.EXPECTED_ITEM_TEXT = 'A new list item'
        self.request = HttpRequest()
        self.request.method = 'POST'
        self.request.POST['item_text'] = self.EXPECTED_ITEM_TEXT

    def test_rootURL_resolvesToHomePageView(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_only_saves_items_when_they_exist_in_request(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        # remove CSRF token to allow us to test
        observed_html = self.remove_csrf_from_markup(response)

        self.assertIn(expected_html, observed_html)

    def test_home_page_can_save_a_POST_request(self):
        home_page(self.request)

        self.assertEqual(Item.objects.count(), 1)
        retrieved_item = Item.objects.first()
        self.assertEqual(retrieved_item.text, self.EXPECTED_ITEM_TEXT)

    def test_home_page_redirects_after_POST(self):
        response = home_page(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text="Itemy 1")
        Item.objects.create(text="Itemy 2")

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('Itemy 1', response.content.decode())
        self.assertIn('Itemy 2', response.content.decode())

    def remove_csrf_from_markup(self, response):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        observed_html = re.sub(csrf_regex, '', response.content.decode())
        return observed_html


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        retrieved_first_item = saved_items[0]
        retrieved_second_item = saved_items[1]
        self.assertEqual(retrieved_first_item.text, first_item.text)
        self.assertEqual(retrieved_second_item.text, second_item.text)
