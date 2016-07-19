from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page

class HomePageTest(TestCase):

	def test_rootURL_resolvesToHomePageView(self):
		found = resolve('/')
		self.assertEquals(found.func, home_page)

