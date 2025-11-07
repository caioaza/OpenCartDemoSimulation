from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from OpenCartDemoSimulation.utilities.BaseClass import BaseClass


class LoginPage(BaseClass):

    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    account_menu = (By.CSS_SELECTOR, "#top .text-end .dropdown .dropdown-toggle")
    login_button = (By.XPATH, "//a[normalize-space()='Login']")
    logout_button = (By.XPATH, "//a[normalize-space()='Logout']")
    email = (By.ID, "input-email")
    password = (By.ID, "input-password")
    submit_button = (By.XPATH, "//button[normalize-space()='Login']")
    login_error = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")

    def open_menu_myaccount(self):
        self.safe_click(LoginPage.account_menu)

    def open_login_page(self):
        login_button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Login']"))
        )
        return login_button.click()
        #return self.driver.find_element(*LoginPage.login_button).click()

    def enter_credentials(self, email, password):
        """Fills in login credentials."""
        self.wait.until(expected_conditions.presence_of_element_located(self.email)).send_keys(email)
        self.wait.until(expected_conditions.presence_of_element_located(self.password)).send_keys(password)

    def get_email_field(self):
        return self.driver.find_element(*LoginPage.email)

    def get_password_field(self):
        return self.driver.find_element(*LoginPage.password)

    def click_submit(self):
        self.safe_click(LoginPage.submit_button)

    def get_login_error(self):
        try:
            return self.wait.until(expected_conditions.visibility_of_element_located(LoginPage.login_error)).text
        except TimeoutException:
            return None

    def get_logout_button(self):
        return self.driver.find_element(*LoginPage.logout_button)

    def check_if_logout_button(self):
        try:
            return self.driver.find_element(*LoginPage.logout_button).is_displayed()
        except NoSuchElementException:
            return False  # If element is not found, return False instead of failing

    def login(self, email, password):
        """Reusable login function to avoid duplication."""
        self.open_menu_myaccount()

        if self.check_if_logout_button():
            self.get_logout_button().click()
            self.open_menu_myaccount()

        self.open_login_page()
        self.enter_credentials(email, password)
        self.click_submit()


