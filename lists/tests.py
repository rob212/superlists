from django.test import TestCase

class SmokeTest(TestCase):

	def test_Runnable(self):
		self.assertEquals(1 + 1, 3)
