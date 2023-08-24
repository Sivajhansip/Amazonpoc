from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')

    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("Installing ChromeDriver...")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), options=chrome_options))


def get_edge_driver():
    try:
        return webdriver.Edge()
    except Exception as e:
        print("Installing Edge driver")
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))


def get_firefox_driver():
    try:
        return webdriver.Firefox()
    except Exception as e:
        print("Installing firefox driver")
        return webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
        # return webdriver.Firefox(executable_path=GeckoDriverManager().install())
