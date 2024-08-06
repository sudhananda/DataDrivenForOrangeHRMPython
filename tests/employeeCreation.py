import time

import pytest
from framework.WebEventUtilities import Driver, WebValidations, WebEvents
from framework.DataUtil import *
from selenium.webdriver.chrome.webdriver import WebDriver


class CommonMethods:
    @classmethod
    def setup_class(cls):
        driver = Driver("chrome")
        cls.driver = driver.get()
        cls.events = WebEvents(driver.get())
        cls.validations = WebValidations(driver.get())
        cls.env_data = get_environment_data("qa")
        driver.launch_application(cls.env_data['url'])

    @classmethod
    def teardown_class(cls):
        time.sleep(10)
        cls.logout(cls)

    def logout(self):
        self.events.click_element(locator=("xpath", "//li[@class='oxd-userdropdown']"))
        self.events.click_element(locator=("xpath", "//a[text()='Logout']"))
        time.sleep(10)
        self.driver.quit()

    @pytest.mark.order(0)
    def test_login(self):
        self.events.enter_text(locator=("name", "username"), value=self.env_data['username'])
        self.events.enter_text(locator=("name", "password"), value=self.env_data['password'])
        self.events.click_element(locator=("xpath", "//button"))
        time.sleep(5)


class EmployeeCommons(CommonMethods):
    def navigate_to_PIM(self):
        self.events.click_element(locator=("xpath", "//span[text()='PIM']"))
        assert self.validations.verify_element_displayed("xpath", "//h5[text()='Employee Information']"), \
            "Application is NOT navigated to Employee List Page"
        time.sleep(5)

    def navigate_to_add_employee(self):
        self.events.click_element(locator=("xpath", "//a[text()='Add Employee']"))
        time.sleep(5)
        assert self.validations.verify_element_displayed("xpath", "//h6[text()='Add Employee']"), \
            "Not navigated to Add Employee Page"

    def enter_employee_basic_info(self, firstName, lastName, emp_id=None, middleName=None):
        self.events.enter_text(locator=("name", "firstName"), value=firstName)
        self.events.enter_text(locator=("name", "lastName"), value=lastName)
        if middleName:
            self.events.enter_text(locator=("name", "middleName"), value=middleName)

        if emp_id:
            self.events.clear_value(locator=("xpath", "//*[text()='Employee Id']/../following-sibling::div/input"),
                                    force_clear=True)
            self.events.enter_text(locator=("xpath", "//*[text()='Employee Id']/../following-sibling::div/input"),
                                   value=emp_id)

    def enter_employee_credentials(self, user_name, password, status):
        self.events.select_checkbox(locator=("xpath", "//span/preceding-sibling::input"))


@pytest.mark.skip(reason="Skipping temporarily")
class TestEmployeeWithoutCredentials(EmployeeCommons):
    def setup_method(self):
        self.emp_data = get_test_case_data(str(Path(__file__).parent.parent.absolute()) +
                                           '/data/createEmployee_data.csv', 'emp_create_1')

    @pytest.mark.order(1)
    def test_addEmployee(self):
        self.navigate_to_PIM()
        self.navigate_to_add_employee()
        self.enter_employee_basic_info(self.emp_data["first_name"], self.emp_data["last_name"])
        time.sleep(5)
        self.events.click_element(locator=("xpath", "//button[@type='submit']"))
        time.sleep(10)


class TestEmployeeWithCredentials(EmployeeCommons):
    def setup_method(self):
        self.emp_data = get_test_case_data(str(Path(__file__).parent.parent.absolute()) +
                                           '/data/createEmployee_data.csv', 'emp_create_3')

    @pytest.mark.order(1)
    def test_addEmployee(self):
        self.navigate_to_PIM()
        self.navigate_to_add_employee()
        self.enter_employee_basic_info(self.emp_data["first_name"], self.emp_data["last_name"])
        time.sleep(5)
        self.enter_employee_credentials("", "", "")
        self.events.click_element(locator=("xpath", "//button[@type='submit']"))
        time.sleep(10)
