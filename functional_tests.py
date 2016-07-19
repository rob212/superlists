from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitely_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_canStartAList_andRetrieveItLater(self):
		# navigate to the home page
		self.browser.get("http://localhost:8000")
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# User is invited to enter a to-do right away

		# User types "buy apples" into a text box

		# User hits enter on keyboard, the page updates and "buy apples" is now shown as a to-do item

		# There is still a text box on screen inviting the User to add another item. User enters "buy chocolate"

		# The page updates again and both items are now shown in the list

		# User wonders if the site will remember their list and notices a unique URL exists. The User visits the URL and finds the list still exists.

if __name__ == '__main__':
	unittest.main(warnings='ignore')
