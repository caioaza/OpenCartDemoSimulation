from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from OpenCartDemoSimulation.utilities.BaseClass import BaseClass


class Checkout(BaseClass):

    def __init__(self,driver):
        self.driver = driver

    button_new_address = (By.ID, "input-shipping-new")
    first_name = (By.ID, "input-shipping-firstname")
    last_name = (By.ID, "input-shipping-lastname")
    address1 = (By.ID, "input-shipping-address-1")
    city = (By.ID, "input-shipping-city")
    post_code = (By.ID, "input-shipping-postcode")
    country = (By.ID, "input-shipping-country")
    region = (By.ID, "input-shipping-zone")
    button_new_address_continue = (By.ID, "button-shipping-address")
    button_shipping_address = (By.ID, "button-shipping-address")
    button_shipping_address_choose = (By.ID, "button-shipping-methods")
    button_shipping_method_flat = (By.ID, "input-shipping-method-flat-flat")
    button_shipping_method_continue = (By.ID, "button-shipping-method")
    button_payment_method_choose = (By.ID, "button-payment-methods")
    button_payment_cash = (By.ID, "input-payment-method-cod-cod")
    button_payment_method_continue = (By.ID, "button-payment-method")
    checkout_products = (By.CSS_SELECTOR, "#checkout-confirm td a")
    button_confirm_order = (By.CSS_SELECTOR, "#checkout-payment button[type='button']")



    def get_button_new_address(self):
        return self.driver.find_element(*Checkout.button_new_address)

    def get_first_name(self):
        return self.driver.find_element(*Checkout.first_name)

    def get_last_name(self):
        return self.driver.find_element(*Checkout.last_name)

    def get_address1(self):
        return self.driver.find_element(*Checkout.address1)

    def get_city(self):
        return self.driver.find_element(*Checkout.city)

    def get_post_code(self):
        return self.driver.find_element(*Checkout.post_code)

    def get_country(self):
        return Select(self.driver.find_element(*Checkout.country))

    def get_region(self):
        return Select(self.driver.find_element(*Checkout.region))

    def click_button_shipping_address_continue(self):
        return self.safe_click(Checkout.button_new_address_continue)

    def click_button_shipping_address(self):
        return self.safe_click(Checkout.button_shipping_address)

    def click_button_shipping_address_choose(self):
        return self.safe_click(Checkout.button_shipping_address_choose)

    def click_button_payment_method_choose(self):
        return self.safe_click(Checkout.button_payment_method_choose)

    def click_button_shipping_method_continue(self):
        return self.safe_click(Checkout.button_shipping_method_continue)

    def get_button_shipping_method_flat(self):
        return self.wait_for_element(Checkout.button_shipping_method_flat)

    def get_button_payment_cash(self):
        return self.wait_for_element(Checkout.button_payment_cash)

    def click_button_payment_method_continue(self):
        return self.safe_click(Checkout.button_payment_method_continue)

    def get_checkout_products(self):
        return self.driver.find_elements(*Checkout.checkout_products)

    def click_button_confirm_order(self):
        return self.safe_click(Checkout.button_confirm_order)





