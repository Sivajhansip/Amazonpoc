from behave import *
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.config import Environment
from features.utilities.excel_utility import Excel
from features.utilities.Screen_shot import Screenshot
from features.login_page.web_elements import WebElements
from features.utilities.test_logging import test_log

logger = test_log()


@given('I am on the Amazon website')
def step_given_open_amazon_site(context):
    context.driver.implicitly_wait(10)
    context.driver.get(Environment.Amazon_site)
    context.driver.maximize_window()
    message = WebElements.LOGIN_CHECK
    wait = WebDriverWait(context.driver, 10)
    url_check = wait.until(EC.visibility_of_element_located(message))
    file_path = Environment.REPORT_FILE
    excel = Excel(file_path)
    check = "Hello, sign in"
    if check != url_check.text:
        excel.write_data("Verify Amazon User Login", "failed")
    assert check == url_check.text, "invalid homepage"
    context.driver.refresh()


@when('I log in with my Amazon credentials read from excel_file')
def step_when_sign_in_with_credentials(context):
    file_path = Environment.FILE
    workbook = Excel(file_path)
    username = workbook.read_data(2, 1)
    password = workbook.read_data(2, 2)

    # Locate and interact with the elements
    WebDriverWait(context.driver, 60).until(EC.element_to_be_clickable(WebElements.SIGN_IN))
    signin_field = context.driver.find_element(By.ID, WebElements.SIGN_IN[1])
    signin_field.click()

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.USERNAME_INPUT))
    username_field = context.driver.find_element(By.ID, WebElements.USERNAME_INPUT[1])
    username_field.clear()  # Clear any existing value
    username_field.send_keys(username)

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.CONTINUE))
    continue_button = context.driver.find_element(By.ID, WebElements.CONTINUE[1])
    continue_button.click()

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.PASSWORD_INPUT))
    password_field = context.driver.find_element(By.ID, WebElements.PASSWORD_INPUT[1])
    password_field.clear()  # Clear any existing value
    password_field.send_keys(password)

    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.SIGN_IN_BUTTON))
    submit_button = context.driver.find_element(By.ID, WebElements.SIGN_IN_BUTTON[1])
    submit_button.click()


@when('I should be logged in successfully')
def step_then_logged_in_successfully(context):
    welcome_message_locator = WebElements.LOGIN_CHECK
    wait = WebDriverWait(context.driver, 20)
    welcome_message = wait.until(EC.visibility_of_element_located(welcome_message_locator))
    file_path = Environment.REPORT_FILE
    excel = Excel(file_path)
    check = "Hello, jansi"

    if check == welcome_message.text:
        excel.write_data("Verify Amazon User Login", "Passed")
    else:
        excel.write_data("Verify Amazon User Login", "failed")
    assert check == welcome_message.text, "Login was failed"
    sc = Screenshot()
    sc.capture_screenshot(context.driver, "reports/Screenshots/", name="homepage")


@when(u'I click on the All icon in the middle of the web page with the search box')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located(WebElements.CLICK_ALL))
    all_icon = context.driver.find_element(By.CSS_SELECTOR, WebElements.CLICK_ALL[1])
    all_icon.click()


@when(u'I enter product name into the search box')
def step_impl_enter_text_into_search_box(context):
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located(WebElements.SEARCH_BOX))
    context.driver.find_element(By.CSS_SELECTOR, WebElements.SEARCH_BOX[1]).send_keys(Environment.PRODUCT_NAME)
    WebDriverWait(context.driver, 100).until(EC.visibility_of_all_elements_located(WebElements.CLICK_ITEM))
    products = context.driver.find_elements(By.CSS_SELECTOR, WebElements.CLICK_ITEM[1])
    for product in products:
        if product.text == Environment.PRODUCT_NAME:
            product.click()
            break
    else:
        assert False, "Product with the text 'laptop' not found"


@when(u'I select required brand under the Brands section on the left scroll bar tab')
def step_impl_select_boAT_from_brands(context):
    WebDriverWait(context.driver, 10).until(EC.presence_of_all_elements_located(WebElements.CHECK_BOX))

    checkboxes = context.driver.find_elements(By.CSS_SELECTOR, WebElements.CHECK_BOX[1])
    brand_found = False
    for check in checkboxes:
        brand_name_element = check.find_element(By.XPATH, WebElements.PRODUCT_NAME[1].format(Environment.BRAND_NAME))
        if brand_name_element.text == Environment.BRAND_NAME:
            brand_name_element.click()
            brand_found = True
            break
    assert brand_found, "Brand 'Samsung' not found in the Brands section"


@then(u'I select the third product from the results')
def select_impl(context):
    WebDriverWait(context.driver, 60).until(EC.presence_of_all_elements_located(WebElements.RESULT))

    search_results = context.driver.find_elements(By.CSS_SELECTOR, WebElements.RESULT[1])
    if len(search_results) >= 3:
        try:
            product_to_select = search_results[2]
            context.product_identifier = product_to_select.get_attribute(WebElements.PRODUCT_ID)
            # print("Selected product identifier:", context.product_identifier)
            logger.info("Selected product identifier: %s", context.product_identifier)
            product_to_select.find_element(By.CSS_SELECTOR, WebElements.PRODUCT_IMAGE[1]).click()
            context.open_window = context.driver.window_handles
            context.driver.switch_to.window(context.open_window[1])

        except ElementClickInterceptedException:
            # print("Element click intercepted. Trying again...")
            logger.warning("Element click intercepted. Trying again...")

    else:
        raise Exception("Less than 3 search results found.")

    assert context.product_identifier is not None, "Product identifier not stored in context.product_identifier"


@then(u'I ensure that the same product is not already added in the cart')
def verify_cart_impl(context):
    product_identifier = context.product_identifier
    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(WebElements.CART_CLICK))
    cart_icon = context.driver.find_element(By.ID, WebElements.CART_CLICK[1])
    cart_icon.click()
    cart_count = context.driver.find_element(By.ID, WebElements.CART_COUNT[1])
    count = int(cart_count.text)
    if count == 0:
        context.product_check_flag = True

    elif count > 0:
        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.CART_ITEMS))
        context.driver.refresh()
        cart_items = context.driver.find_elements(By.XPATH, WebElements.CART_ITEMS[1])
        for item in cart_items:
            item_identifier = item.get_attribute(WebElements.PRODUCT_ID)
            if item_identifier == product_identifier:
                # print("The product is already in the cart.")
                logger.info("The product is already in the cart.")
                try:
                    quantity_dropdown = item.find_element(By.XPATH, WebElements.DROP_DOWN[1])
                    current_quantity = int(quantity_dropdown.text)
                    # print("current_quantity:", current_quantity)
                    logger.debug("current_quantity:%d", current_quantity)
                    if current_quantity > 1:
                        dropdown = Select(item.find_element(By.ID, WebElements.QUANTITY[1]))
                        dropdown.select_by_visible_text("1")
                        # print("The product quantity is now 1. Skipping adding to cart.")
                        logger.info("The product quantity is now 1. Skipping adding to cart.")
                        context.product_check_flag = False
                        current_quantity = 1
                    elif current_quantity == 1:
                        context.product_check_flag = False
                        # print("The product quantity is already 1. Skipping adding to cart.")
                        logger.info("The product quantity is already 1. Skipping adding to cart.")
                        current_quantity = 1
                    context.product_added_to_cart = True
                    context.quantity = current_quantity
                    # context.product_added_to_cart=True
                except Exception as e:
                    # print("Could not update the quantity or remove the duplicate product from the cart:", repr(e))
                    logger.warning("Could not update the quantity or remove the duplicate product from the cart:%s",
                                   repr(e))
            else:
                # print("product doesn't match")
                logger.info("product doesn't match")
                context.product_check_flag = True
                context.quantity = 1
                break


@then(u'I click on "Add to Cart"')
def add_to_cart(context):
    if context.product_check_flag:

        product_identifier = context.product_identifier
        # print("Stored product identifier:", product_identifier)
        logger.info("Stored product identifier:%s", product_identifier)
        try:
            cart_count_element = WebDriverWait(context.driver, 30).until(
                EC.visibility_of_element_located(WebElements.CART_COUNT))
            initial_cart_count = int(cart_count_element.text)
            # print(initial_cart_count)
            logger.debug("initial cart count:%d", initial_cart_count)
            context.driver.back()
            add_to_cart_button = WebDriverWait(context.driver, 20).until(
                EC.element_to_be_clickable(WebElements.ADD_TO_CART_BUTTON))

            # print("Add to Cart button text:", add_to_cart_button.get_attribute(WebElements.TITLE))
            # print("Add to Cart button is enabled:", add_to_cart_button.is_enabled())
            logger.info("Add to Cart button text:%s", add_to_cart_button.get_attribute(WebElements.TITLE))
            logger.info("Add to Cart button is enabled:%s", add_to_cart_button.is_enabled())
            add_to_cart_button.click()
            try:
                view_cart_button = WebDriverWait(context.driver, 20).until(
                    EC.element_to_be_clickable(WebElements.VIEW_CART))
                view_cart_button.click()
            except:
                view_cart_button = WebDriverWait(context.driver, 20).until(
                    EC.element_to_be_clickable(WebElements.CART_CLICK))
                view_cart_button.click()
            updated_cart_count_element = context.driver.find_element(By.ID, WebElements.CART_COUNT[1])
            updated_cart_count = int(updated_cart_count_element.text)
            logger.info("updated cart count:%d", updated_cart_count)
            # print("updated cart count:", updated_cart_count)
            if updated_cart_count > initial_cart_count:
                # print("Product added to cart successfully.")
                logger.info("Product added to cart successfully.")
                context.product_added_to_cart = True
                context.quantity = 1
            else:
                # print("An error occurred while adding the product to the cart: Cart count not updated.")
                logger.warning("An error occurred while adding the product to the cart: Cart count not updated.")
                logger.debug("Expected cart count:%d", initial_cart_count + 1)
                logger.debug("Actual cart count:%d", updated_cart_count)
                # print("Expected cart count:", initial_cart_count + 1)
                # print("Actual cart count:", updated_cart_count)
                context.product_added_to_cart = False
        except Exception as e:
            # print(repr(e))
            logger.warning("exception:%s", repr(e))

    assert context.product_added_to_cart, "Product was not added to the cart"


@then(u'only a single product should be added to the cart')
def verify_single_product_added(context):
    if context.quantity == 1:
        context.product_added_to_cart = True
    else:
        try:
            verify_cart_impl(context)
            context.product_added_to_cart = True
            context.quantity = 1
        except:
            raise Exception("multiple products in cart verify cart functionality is not working correctly")
    assert context.product_added_to_cart, "Product was not added to the cart"


@then(u'I click on "Proceed to Checkout"')
def proceed_to_checkout(context):
    if context.product_added_to_cart:

        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.DATA_ASIN))

        product_identifier = context.product_identifier
        cart_items = context.driver.find_elements(By.XPATH, WebElements.DATA_ASIN[1])

        items_to_remove = []

        for item in cart_items:
            item_identifier = item.get_attribute(WebElements.ITEM)
            if item_identifier != product_identifier:
                items_to_remove.append(item_identifier)
            else:
                pass
        # print(items_to_remove)
        logger.info(items_to_remove)
        for item_identifier in items_to_remove:
            try:
                delete_button_locator = (By.XPATH, WebElements.delete_button_xpath_template.format(item_identifier))
                delete_button = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable(delete_button_locator))
                delete_button.click()
                logger.info("Removed product:%s", item_identifier)
                # print("Removed product:", item_identifier)
                context.driver.refresh()
            except NoSuchElementException:
                logger.warning("This is the product we want to keep:%s", item_identifier)
                # print("This is the product we want to keep:", item_identifier)
                context.driver.refresh()

        WebDriverWait(context.driver, 10).until(EC.presence_of_element_located(WebElements.DATA_ASIN))
        context.driver.refresh()
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located(WebElements.CHECKOUT))
        checkout = context.driver.find_element(By.CSS_SELECTOR, WebElements.CHECKOUT[1])
        checkout.click()
        context.driver.refresh()
        # print("proceed to checkout was clicked")
        logger.info("proceed to checkout was clicked")

    else:
        raise Exception("It is not entering to if block")
    expected_text_in_checkout_page = "Checkout"
    checkout_h1_element = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    actual_text_in_checkout_page = checkout_h1_element.text
    # print("Expected Checkout-", expected_text_in_checkout_page)
    # print("Actual text", actual_text_in_checkout_page)
    logger.debug("Expected Checkout-%s", expected_text_in_checkout_page)
    logger.debug("Actual text %s", actual_text_in_checkout_page)
    assert expected_text_in_checkout_page.lower() == actual_text_in_checkout_page.lower(), "Failed to proceed to checkout"
    sc = Screenshot()
    sc.capture_screenshot(context.driver, "reports/Screenshots/", name="after checkout")


@then('I should be taken to the checkout page for further steps in the purchase process')
def further_steps(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located(WebElements.PLACE_ORDER))
    address = context.driver.find_element(By.CSS_SELECTOR, WebElements.PLACE_ORDER[1])
    address.click()
    sc = Screenshot()
    sc.capture_screenshot(context.driver, "reports/Screenshots/", name="Before payment")
