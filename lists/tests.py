import re
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List


class HomePageTest(TestCase):
	def setUp(self):
		self.request = HttpRequest()
		self.request.method = 'POST'
		self.request.POST['item_text'] = 'A new list item'

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

	def remove_csrf_from_markup(self, response):
		csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
		observed_html = re.sub(csrf_regex, '', response.content.decode())
		return observed_html


class ListViewTest(TestCase):
	def test_displays_only_items_for_that_list(self):
		my_list = List.objects.create()
		Item.objects.create(text="Itemy 1", list=my_list)
		Item.objects.create(text="Itemy 2", list=my_list)

		other_list = List.objects.create()
		Item.objects.create(text="Other list item 1", list=other_list)
		Item.objects.create(text="Other list item 2", list=other_list)

		response = self.client.get('/lists/%d/' % my_list.id)

		self.assertContains(response, "Itemy 1")
		self.assertContains(response, "Itemy 2")
		self.assertNotContains(response, "Other list item 1")
		self.assertNotContains(response, "Other list item 2")

	def test_list_template_is_being_used(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % list_.id)
		self.assertTemplateUsed(response, 'list.html')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % correct_list.id)
		self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		retrieved_item = Item.objects.first()
		self.assertEqual(retrieved_item.text, 'A new list item')

	def test_redirects_after_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % new_list.id)


class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		self.client.post('/lists/%d/add_item' % correct_list.id, data={'item_text': 'A new item for an existing list'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		response = self.client.post('/lists/%d/add_item' % correct_list.id,
		                            data={'item_text': 'A new item for an existing list'})

		self.assertRedirects(response, '/lists/%d/' % correct_list.id)


class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		my_list = List()
		my_list.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = my_list
		first_item.save()

		second_item = Item()
		second_item.text = 'The second item'
		second_item.list = my_list
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, my_list)

		saved_items = Item.objects.all()
		self.assertEquals(saved_items.count(), 2)

		retrieved_first_item = saved_items[0]
		retrieved_second_item = saved_items[1]
		self.assertEqual(retrieved_first_item.text, first_item.text)
		self.assertEqual(retrieved_first_item.list, my_list)
		self.assertEqual(retrieved_second_item.text, second_item.text)
		self.assertEqual(retrieved_second_item.list, my_list)
