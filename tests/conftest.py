import os
import time

import pytest
import logging
from selenium import webdriver
from pytest_html import extras  # Import pytest_html extras
import logging
from selenium.common.exceptions import SessionNotCreatedException

from OpenCartDemoSimulation.pageObjects.LoginPage import LoginPage
from OpenCartDemoSimulation.pageObjects.ProductsPage import ProductsPage
from OpenCartDemoSimulation.tests.test_login import TestLogin
from OpenCartDemoSimulation.utilities.configurations import user_opencart_credentials


#method found on pytest docs to pass command line options at run time in terminal. Adapted to call multiple browsers when testing
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome",
        choices=["chrome", "firefox", "edge"],  # Restrict to valid options
        help="Choose browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--url", action="store", default="http://localhost/opencart/",
        help="Specify the base URL for testing"
    )

#scope class makes it be executed only once when class is called
@pytest.fixture(scope="class", params=[
    (375, 812),   # iPhone X
    #(414, 896),   # iPhone XR
   # (768, 1024),  # iPad
   # (1024, 768),  # Small Laptop
  #  (1366, 768),  # Standard Laptop
])
def setup(request):
     # IMPORTANT: Because of the fixes to skip recaptcha, before runing the tests, all the Chrome windows need to be closed: taskkill /IM chrome.exe /F (windows command) 
    browser_name = request.config.getoption("browser_name")
    url = request.config.getoption("url")
    width, height = request.param
    driver = None  # Initialize driver variable

    try:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")  # Run Chrome in headless mode (doesn't open browser)
            #options.add_argument("--disable-gpu")  # Recommended for headless mode on Windows
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            driver = webdriver.Edge(options=options)

        driver.implicitly_wait(4)  # It tells Selenium to wait up to 4 seconds for an element to appear before throwing an exception (e.g., NoSuchElementException). It applies to all find_element or find_elements calls
        driver.set_window_size(width, height)
        driver.get(url)
        request.cls.driver = driver
        yield driver #returns driver

    except SessionNotCreatedException as e:
        print(f"SessionNotCreatedException: {e.msg}")  # Print only the relevant error message
    except Exception as e:
        print(f"Error: {str(e).splitlines()[-1]}")  # Print only the last line of the error message

    finally:
        if driver:
            driver.quit()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #Attach logs and screenshots to the HTML report
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is None:
        return  # Exit the function if pytest-html is not available

    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    # Attach logs to report

    # Define the reports directory (one level up from 'tests/')
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
    log_file = os.path.join(reports_dir, "logfile.log")  # Save in reports folder

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    try:
        with open(log_file, "r") as f:
            log_content = f.read().strip()
        if log_content:
            extra.append(extras.text(log_content, "Test Logs"))
    except Exception as e:
        logging.error(f"Error attaching logs: {e}")

    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")

    # Capture and attach screenshot on failure
    if report.when in ["call", "setup"]:
        xfail = hasattr(report, "wasxfail")
        if (report.failed and not xfail) or (report.skipped and xfail):
            if hasattr(item.cls, "driver"):
                file_name = report.nodeid.replace("::", "_") + ".png"
                file_path = os.path.join(reports_dir, file_name)  # Save in reports folder
                _capture_screenshot(item.cls.driver, file_path)
                if file_name:
                    html = f'<div><img src="../reports/{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>'
                    extra.append(extras.html(html))

    report.extra = extra


def _capture_screenshot(driver, name):
    #Take a screenshot if WebDriver is available
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
    screenshot_path = os.path.join(reports_dir, name)  # Save inside reports folder
    try:
        driver.get_screenshot_as_file(screenshot_path)
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")

@pytest.fixture
def logged_in_user(setup): #setup contains driver
    login_page = LoginPage(setup)
    email = user_opencart_credentials["email"]
    password = user_opencart_credentials["password"]
    login_page.login(email=email,password=password)
    time.sleep(3)
    return setup  # driver is now in an authenticated session

@pytest.fixture
def cart_with_products(logged_in_user): # Pytest sees that cart_with_product needs something named logged_in_user, so before running cart_with_product, it runs logged_in_user first and returns whatever that fixture returned, in this case: driver
    products_page = ProductsPage(logged_in_user) #logged_in_user contains driver
    products_to_cart = {"iPod Classic", "iPod Nano", "iPod Touch"}
    products_page.add_products_to_the_cart(products_to_cart)
    return logged_in_user  # driver now has 3 items in cart, ready for checkout
