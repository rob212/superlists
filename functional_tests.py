from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])


	def test_can_start_a_list_add_two_items_and_retrieve_it_later(self):
		# navigate to the home page
		self.browser.get("http://localhost:8000")
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# User is invited to enter a to-do right away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a new to-do item')

		# User types "buy apples" into a text box
		inputbox.send_keys("buy apples")

		# User hits enter on keyboard, the page updates and "buy apples" is now shown as a to-do item
		inputbox.send_keys(Keys.ENTER)

		self.check_for_row_in_table('1: buy apples')

		#  There is still a text box on screen inviting the User to add another item. User enters "buy chocolate"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("buy chocolate")
		inputbox.send_keys(Keys.ENTER)

		# The page updates again and both items are now shown in the list
		self.check_for_row_in_table('2: buy chocolate')

		# User wonders if the site will remember their list and notices a unique URL exists.
		# The User visits the URL and finds the list still exists.
		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
