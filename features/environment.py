import os
import datetime
import allure
from features.drivers.driver_setup import *
from features.steps.config import Environment


def before_all(context):
    if Environment.BROWSER == "Chrome":
        context.driver = get_chrome_driver()
    elif Environment.BROWSER == "Edge":
        context.driver = get_edge_driver()
    elif Environment.BROWSER == "Firefox":
        context.driver = get_firefox_driver()
    context.product_identifier = None
    context.product_check_flag = False
    context.product_added_to_cart = False
    context.quantity = 0


def after_step(context, step):
    if step.status == 'failed':
        allure.attach(context.driver.get_screenshot_as_png(), name='screenshot_fail',
                      attachment_type=allure.attachment_type.PNG)
    elif step.status == 'passed':
        allure.attach(context.driver.get_screenshot_as_png(), name='screenshot_pass',
                      attachment_type=allure.attachment_type.PNG)


def after_all(context):
    context.driver.quit()

    json_report_folder = "reports/json"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report_folder = os.path.join(json_report_folder, f"HTML_{timestamp}")
    os.system(f"allure generate reports/json -o {json_report_folder} --clean")
