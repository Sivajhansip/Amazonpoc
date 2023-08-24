from selenium.webdriver.common.by import By
from features.steps.config import Environment


class WebElements:
    SIGN_IN = ["id", 'nav-signin-tooltip']
    USERNAME_INPUT = ["id", 'ap_email']
    CONTINUE = ["id", 'continue']
    PASSWORD_INPUT = ["id", 'ap_password']
    SIGN_IN_BUTTON = ["id", 'signInSubmit']
    LOGIN_CHECK = [By.CSS_SELECTOR, '#nav-link-accountList-nav-line-1']
    CLICK_ALL = [By.CSS_SELECTOR, ".nav-search-scope"]
    SEARCH_BOX = [By.CSS_SELECTOR, "#twotabsearchtextbox"]
    CLICK_ITEM = [By.CSS_SELECTOR, ".s-suggestion-container"]
    CHECK_BOX = [By.CSS_SELECTOR, ".a-icon"]
    PRODUCT_NAME = [By.XPATH, "//span[text()='{}']"]
    RESULT = [By.CSS_SELECTOR, ".s-asin"]
    PRODUCT_ID = "data-asin"
    PRODUCT_IMAGE = [By.CSS_SELECTOR, ".s-image"]
    CART_CLICK = [By.ID, "nav-cart"]
    CART_COUNT = [By.ID, "nav-cart-count"]
    CART_ITEMS = [By.XPATH, "//div[@data-asin]"]
    DROP_DOWN = [By.XPATH, ".//span[@class='a-dropdown-prompt']"]
    QUANTITY = [By.ID, "quantity"]
    ADD_TO_CART_BUTTON = [By.ID, "add-to-cart-button"]
    VIEW_CART = [By.CSS_SELECTOR, "input[aria-labelledby='attach-sidesheet-view-cart-button-announce']"]
    DATA_ASIN = [By.XPATH, "//div[@data-asin]"]
    ITEM = "data-asin"
    TITLE = "title"
    CHECKOUT = [By.CSS_SELECTOR, "#desktop-ptc-button-celWidget"]
    delete_button_xpath_template = "//div[@data-asin='{}']//input[@value='Delete']"
    PLACE_ORDER = [By.CSS_SELECTOR, "#orderSummaryPrimaryActionBtn"]
