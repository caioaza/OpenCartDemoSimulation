from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from OpenCartDemoSimulation.pageObjects.ProductsPage import ProductsPage
from OpenCartDemoSimulation.utilities.BaseClass import BaseClass


class CartPage(BaseClass):

    def __init__(self,driver):
        self.driver = driver
        # Create a ProductsPage instance and store it
        self.products_page = ProductsPage(driver)


    products = (By.CSS_SELECTOR, "#output-cart table tbody tr")
    product_title = (By.CSS_SELECTOR, "td.text-start a")
    product_quantity = (By.CSS_SELECTOR, "input[name='quantity']")
    product_price_unit = (By.CSS_SELECTOR, "td:nth-child(4)")
    product_price_total = (By.CSS_SELECTOR, "td:nth-child(5)")
    product_remove_button = (By.CSS_SELECTOR, "div.input-group > button:last-of-type")
    product_update_quantity_button = (By.CSS_SELECTOR, "div.input-group > button:first-of-type")
    subtotal = (By.CSS_SELECTOR, "#checkout-total tr:nth-child(1) td:nth-child(2)")
    checkout_button = (By.XPATH, "//div[@id='shopping-cart']//a[normalize-space()='Checkout']")


    def get_products(self):
        return self.driver.find_elements(*CartPage.products)

    def get_product_title(self, product):
        return product.find_element(*CartPage.product_title).text

    def get_product_quantity(self, product):
        return product.find_element(*CartPage.product_quantity)

    def get_product_price_unit(self, product):
        return product.find_element(*CartPage.product_price_unit).text

    def get_product_price_total(self, product):
        return product.find_element(*CartPage.product_price_total).text

    def get_checkout_buttons(self):
        # Using find_elements here instead of find_element because if there's no checkout button I'll have an empty list only instead of an error of no such element, if it was with find_element
        return self.driver.find_elements(*CartPage.checkout_button)

    def click_checkout_button(self):
        self.safe_click(CartPage.checkout_button)

    def click_update_quantity_button(self, product):
        return product.find_element(*CartPage.product_update_quantity_button).click()

    def get_subtotal(self):
        return self.driver.find_element(*CartPage.subtotal).text

    def update_quantity(self, product_row, new_quantity):
        quantity_input = product_row.find_element(*CartPage.product_quantity)
        quantity_input.clear()
        quantity_input.send_keys(str(new_quantity))
        self.click_update_quantity_button(product_row)

    def contains_product(self, name):
        for product in self.get_products():
            if self.get_product_title(product) == name:
                return True
        return False

    def remove_products_from_the_cart(self):
        get_page_title = self.driver.title
        if get_page_title != "Shopping Cart":
            self.products_page.click_cart_button()
        # Checks if cart is empy and if it's not, delete the items
        # Continuously remove products until the cart is empty. After each product removal, it gets all products again, because the DOM is updating all the products after each removal. Avoids stale elements by re-fetching the cart products on every loop.
        while True:
            cart_products = self.get_products()
            if not cart_products:
                break

            # Grab the first product row
            product_row = cart_products[0]

            # Find the remove button within that product row
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-danger[title='Remove']"))
            )
            remove_button.click()

            # Wait until the specific product row is no longer attached to the DOM
            WebDriverWait(self.driver, 10).until(EC.staleness_of(product_row))

