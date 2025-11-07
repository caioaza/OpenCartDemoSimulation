import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from OpenCartDemoSimulation.pageObjects.CartPage import CartPage
from OpenCartDemoSimulation.utilities.BaseClass import BaseClass
from OpenCartDemoSimulation.pageObjects.Checkout import Checkout
from OpenCartDemoSimulation.utilities.mock_data import generate_shipping_address

class TestCheckout(BaseClass):

    def test_e2e_registered_user_creates_successful_order(self,cart_with_products):
        cart_page = CartPage(cart_with_products) #cart_with_products is a pytest fixture
        cart_page.click_checkout_button()
        checkout_page = Checkout(self.driver)
        checkout_page.get_button_new_address().click()
        shipping_address = generate_shipping_address()
        shipping_address_first_name = shipping_address["first_name"]
        shipping_address_last_name = shipping_address["last_name"]
        shipping_address_address = shipping_address["address"]
        shipping_address_city = shipping_address["city"]
        shipping_post_code = shipping_address["post_code"]
        checkout_page.get_first_name().send_keys(shipping_address_first_name)
        checkout_page.get_last_name().send_keys(shipping_address_last_name)
        checkout_page.get_address1().send_keys(shipping_address_address)
        checkout_page.get_city().send_keys(shipping_address_city)
        checkout_page.get_post_code().send_keys(shipping_post_code)
        select_country = checkout_page.get_country()
        select_country.select_by_visible_text("Ireland")
        select_region = checkout_page.get_region()
        select_region.select_by_visible_text("Dublin")
        checkout_page.click_button_shipping_address_continue()
        time.sleep(1) # allow shipping methods to be updated
        checkout_page.click_button_shipping_address_choose()
        checkout_page.get_button_shipping_method_flat().click()
        checkout_page.click_button_shipping_method_continue()
        checkout_page.click_button_payment_method_choose()
        checkout_page.get_button_payment_cash().click()
        checkout_page.click_button_payment_method_continue()

        assert len(checkout_page.get_checkout_products()) == 3, "Number of products to checkout isn't correct."

        checkout_page.click_button_confirm_order()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains("checkout/success"))

        assert "checkout/success" in self.driver.current_url, f"Expected to be on checkout success page, but got {self.driver.current_url}"



    def test_checkout_cannot_place_order_without_payment_method(self):
        pass


    def test_checkout_cannot_place_order_without_shipping_method(self):
        pass