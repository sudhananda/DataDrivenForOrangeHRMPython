from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import Edge
from selenium.webdriver import Safari
from selenium.webdriver.chrome.webdriver import WebDriver
from framework.exceptions import (InvalidBrowserException, FailedToEnterValueException,
                                  SelectValueFromListFailedException, FailedToClearValueException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementClickInterceptedException,
                                        NoSuchElementException, TimeoutException, ElementNotInteractableException
                                        )


class Driver:
    def __init__(self, browser):
        self.browser = browser
        self.driver = None

        if browser == "chrome":
            self.driver = Chrome()
        elif browser == "firefox":
            self.driver = Firefox()
        elif browser == "edge":
            self.driver = Edge()
        elif browser == "safari":
            self.driver = Safari
        else:
            raise InvalidBrowserException("Given browser '" + browser + "' is invalid. please provide a valid browser."
                                                                        " anyone in (chrome,firefox, edge,safari)")

        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

    def get(self):
        return self.driver

    def launch_application(self, url: str):
        self.driver.get(url)


class WebEvents:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def get_element(self, locator_name, locator_value):
        try:
            return self.wait.until(EC.presence_of_element_located((locator_name, locator_value)))
        except Exception:
            return None

    def click_element(self, element: WebElement = None, locator=tuple(), wait_time=10):
        def click(elem: WebElement):
            try:
                elem.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                self.driver.execute_script("arguments[0].click()", elem)

        if element is not None:
            click(element)
        elif locator:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            click(element)
        else:
            raise ValueError("Either an element or a valid locator must be provided.")

    def enter_text(self, element: WebElement = None, value="", locator=tuple(), wait_time=10, force_enter=False):
        def enter(elem: WebElement):
            try:
                elem.send_keys(value)
            except ElementNotInteractableException:
                if force_enter:
                    self.driver.execute_script("arguments[0].setAttribute('value','" + value + "');", elem)
                else:
                    raise FailedToEnterValueException(
                        "Unable to enter the value into the field as the field is either disabled or not visible.")

        if element:
            enter(element)
        elif locator:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            enter(element)
        else:
            raise ValueError("Either an element or a valid locator must be provided.")

    def clear_value(self, element: WebElement = None, locator=tuple(), wait_time=10, force_clear=False):
        def clear(elem: WebElement):
            try:
                elem.clear()
            except ElementNotInteractableException:
                if force_clear:
                    self.driver.execute_script("arguments[0].setAttribute('value','');", elem)
                else:
                    raise FailedToClearValueException(
                        "Unable to enter the value into the field as the field is either disabled or not visible.")

        if element:
            clear(element)
        elif locator:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            clear(element)
        else:
            raise ValueError("Either an element or a valid locator must be provided.")

    def select_checkbox(self, element: WebElement = None, locator=tuple(), wait_time=10):
        def select(elem: WebElement):
            if not elem.is_selected():
                try:
                    elem.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click()", elem)
                except ElementNotInteractableException:
                    print("Unable to select the checkbox as the checkbox is disabled.")
            else:
                print("Checkbox is already selected.")

        if element:
            select(element)
        elif locator:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            select(element)
        else:
            raise ValueError("Either an element or a valid locator must be provided.")

    def select_value_from_list(self, element: WebElement = None, locator=tuple(), value="", wait_time=10):
        def select(elem: WebElement):
            options_list = elem.find_elements(By.TAG_NAME, "option")  # change this tag name as per application
            option_found = False
            for opt in options_list:
                if opt.text.lower().strip() == value.lower().strip():
                    opt.click()
                    option_found = True
                    break

            if not option_found:
                raise SelectValueFromListFailedException()

        if element:
            select(element)
        elif locator:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(*locator))
            select(element)
        else:
            raise ValueError("Either an element or a valid locator must be provided.")


class WebValidations:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def verify_element_displayed(self, by, value):
        elem_count = len(self.driver.find_elements(by, value))
        if elem_count > 0:
            return True
        else:
            return False
