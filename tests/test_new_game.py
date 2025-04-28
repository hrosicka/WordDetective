import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewGameTests(unittest.TestCase):
    """
    This class contains unit tests for the 'New Game' functionality of the web application.
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

    def test_start_new_game_link_changes_clues(self):
        """
        This test verifies that clicking the 'Start New Game' link results in a change
        in the text content of the clues container. It checks that the clues are
        different after a new game is initiated.
        """
        # Locate the 'Start New Game' link and wait for it to be present.
        new_game_link = self.wait.until(EC.presence_of_element_located((By.ID, 'start-new-game-link')))
        # Locate the container that holds the clues.
        clues_container = self.driver.find_element(By.CLASS_NAME, 'clues-container')
        # Get the initial text content of the clues container.
        initial_clues_text = clues_container.text
        # Click the 'Start New Game' link to initiate a new game.
        new_game_link.click()
        # Wait for the clues container to have its text content changed (in this case, to be empty temporarily).
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'clues-container'), ''))
        # Get the text content of the clues container after clicking the link.
        new_clues_text = self.driver.find_element(By.CLASS_NAME, 'clues-container').text
        # Assert that the new clues text is not the same as the initial clues text,
        # indicating that a new set of clues has been loaded.
        self.assertNotEqual(new_clues_text, initial_clues_text)

if __name__ == '__main__':
    unittest.main()