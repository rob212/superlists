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
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
