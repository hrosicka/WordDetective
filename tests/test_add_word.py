import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddWordTests(unittest.TestCase):
    """
    This class contains unit tests for adding a new word to the application's database
    through the hamburger menu navigation.
    """
    def setUp(self):
        """
        Initialize the WebDriver and navigate to the application's homepage.
        """
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:5000/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """
        Quit the WebDriver instance.
        """
        self.driver.quit()

    def test_add_new_word(self):
        """
        This test verifies that a new word can be added through the hamburger menu
        and checks if it appears in the word list afterwards.
        """
        # Open the hamburger menu
        hamburger_menu = self.wait.until(EC.presence_of_element_located((By.ID, 'hamburger-menu')))
        hamburger_menu.click()

        # Navigate to the 'Add Word' page
        add_word_menu_item = self.wait.until(EC.presence_of_element_located((By.ID, 'menu-add-word')))
        add_word_menu_item.click()

        # Locate the input fields for the word and hint
        word_input = self.wait.until(EC.presence_of_element_located((By.ID, 'word')))
        description_input = self.driver.find_element(By.ID, 'description')

        # Enter a new word and hint
        word_input.send_keys('TestingWord')
        description_input.send_keys('Testing Hint')

        # Submit the form
        submit_button = self.driver.find_element(By.ID, 'submit-word-button')
        submit_button.click()

        # Return to the main screen
        home_button = self.wait.until(EC.presence_of_element_located((By.ID, 'home-button')))
        home_button.click()

        # Open the hamburger menu again
        hamburger_menu = self.wait.until(EC.presence_of_element_located((By.ID, 'hamburger-menu')))
        hamburger_menu.click()

        # Navigate to the 'Preview Data' page
        preview_data_menu_item = self.wait.until(EC.presence_of_element_located((By.ID, 'menu-preview-data')))
        preview_data_menu_item.click()

        # Verify that the new word appears in the preview data table
        table = self.wait.until(EC.presence_of_element_located((By.ID, 'dataTable_wrapper')))
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Check if the word is in any row of the table
        word_found = any('TestingWord' in row.text for row in rows)
        self.assertTrue(word_found, 'Testing Hint was not found in the data table')

if __name__ == '__main__':
    unittest.main()