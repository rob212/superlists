from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys


class NewVisitorTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

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
		# Barry navigates to the home page
		self.browser.get(self.server_url)
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# Barry is invited to enter a to-do right away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a new to-do item')

		# Barry types "buy apples" into a text box
		inputbox.send_keys("buy apples")

		# Barry hits enter on keyboard, the page updates and "buy apples" is now shown as a to-do item
		inputbox.send_keys(Keys.ENTER)
		barry_list_url = self.browser.current_url
		self.assertRegex(barry_list_url, '/lists/.+')
		self.check_for_row_in_table('1: buy apples')

		#  There is still a text box on screen inviting the User to add another item. User enters "buy chocolate"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("buy chocolate")
		inputbox.send_keys(Keys.ENTER)

		# The page updates again and both items are now shown in the list
		self.check_for_row_in_table('2: buy chocolate')
		self.check_for_row_in_table('1: buy apples')

		# Now a new user, Karen comes to the site

		## We use a new browser session to make sure that no info of Barry's is present
		##  from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Karen visits the home page, there is no sign of Barry's list
		self.browser.get(self.server_url)
		page_text = self.browser.find_elements_by_tag_name('body')
		self.assertNotIn('1: buy apples', page_text)
		self.assertNotIn('2: but chocolate', page_text)

		# Karen starts her own list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("practice yoga")
		inputbox.send_keys(Keys.ENTER)

		# Karen gets her own unique list URL
		karen_list_url = self.browser.current_url
		self.assertRegex(karen_list_url, '/lists/.+')
		self.assertNotEqual(karen_list_url, barry_list_url)

		self.check_for_row_in_table('1: practice yoga')
		page_text = self.browser.find_elements_by_tag_name('body')
		self.assertNotIn('1: buy apples', page_text)

	def test_layout_and_styling(self):
		# Barry goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		# He notices that the input box is nicely centered
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=5
		)

		# He starts a new list to see if the input box remained centered on
		# the view lists page to
		input_box.send_keys('dance dance dance\n')
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=5
		)


