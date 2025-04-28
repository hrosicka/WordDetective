import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomepageTests(unittest.TestCase):
    """
    This class contains unit tests for the homepage of the web application.
    It uses Selenium WebDriver to interact with the web page.
    """
    def setUp(self):
        """
        Set up method that is called before each test.
        It initializes the Chrome WebDriver and navigates to the application's homepage.
        It also initializes a WebDriverWait object for handling dynamic elements.
        """
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:5000/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """
        Tear down method that is called after each test.
        It quits the WebDriver instance, closing all associated browser windows.
        """
        self.driver.quit()

    def test_homepage_title(self):
        """
        This test verifies that the title of the homepage is correctly set to 'Word Detective'.
        It retrieves the page title using the WebDriver and asserts that it matches the expected value.
        """
        self.assertEqual(self.driver.title, 'Word Detective')

    def test_change_player_link(self):
        """
        This test verifies that clicking the 'Change Player' link navigates the user
        to the correct URL containing 'change_name'. It locates the link, clicks it,
        and then asserts that the current URL of the WebDriver includes the expected string.
        """
        # Locate the 'Change Player' link and wait for it to be present.
        change_player_link = self.wait.until(EC.presence_of_element_located((By.ID, 'change-name-link')))
        # Click the 'Change Player' link.
        change_player_link.click()
        # Assert that the current URL of the browser contains the string 'change_name',
        # indicating that the navigation to the change player page was successful.
        self.assertTrue("change_name" in self.driver.current_url)

if __name__ == '__main__':
    unittest.main()