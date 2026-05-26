"""
Selenium Test Configuration & Fixtures
Shared test setup, fixtures, and utilities for all Selenium tests
"""

import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test import Client
from django.contrib.auth.models import Group, User
from accounts.models import CustomUser
from bookings.models import Booking, AvailabilitySlot
from doctors.models import Doctor


# Test Configuration
BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:8000')
TIMEOUT = 10
HEADLESS = os.getenv('HEADLESS_BROWSER', 'True').lower() == 'true'


@pytest.fixture(scope='session')
def chrome_options():
    """Configure Chrome options for Selenium tests"""
    options = ChromeOptions()
    
    if HEADLESS:
        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    
    return options


@pytest.fixture(scope='function')
def driver(chrome_options):
    """Create and cleanup WebDriver instance for each test"""
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(TIMEOUT)
    driver.set_page_load_timeout(TIMEOUT)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope='function')
def wait(driver):
    """WebDriverWait instance for explicit waits"""
    return WebDriverWait(driver, TIMEOUT)


@pytest.fixture(scope='function')
def test_user(django_db):
    """Create a test user for authentication tests"""
    from django.contrib.auth.models import User
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123!'
    )
    
    # Add to doctors group
    from django.contrib.auth.models import Group
    doctors_group, _ = Group.objects.get_or_create(name='doctors')
    user.groups.add(doctors_group)
    
    return user


@pytest.fixture(scope='function')
def test_patient(django_db):
    """Create a test patient for booking tests"""
    from django.contrib.auth.models import User, Group
    
    user = User.objects.create_user(
        username='testpatient',
        email='patient@example.com',
        password='TestPassword123!'
    )
    
    # Add to patients group
    patients_group, _ = Group.objects.get_or_create(name='patients')
    user.groups.add(patients_group)
    
    return user


@pytest.fixture(scope='function')
def test_doctor(django_db):
    """Create a test doctor for availability tests"""
    from django.contrib.auth.models import User, Group
    from doctors.models import Doctor
    
    user = User.objects.create_user(
        username='testdoctor',
        email='doctor@example.com',
        password='TestPassword123!'
    )
    
    # Add to doctors group
    doctors_group, _ = Group.objects.get_or_create(name='doctors')
    user.groups.add(doctors_group)
    
    # Create doctor profile
    doctor = Doctor.objects.create(
        user=user,
        specialization='General Medicine',
        license_number='LN12345'
    )
    
    return doctor


class SeleniumTestHelper:
    """Helper class for common Selenium operations"""
    
    @staticmethod
    def login(driver, username, password, wait):
        """
        Perform login operation
        
        Args:
            driver: WebDriver instance
            username: Username to login with
            password: Password
            wait: WebDriverWait instance
        """
        driver.get(f'{BASE_URL}/login/')
        
        # Wait for login form
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_field = driver.find_element(By.NAME, 'password')
        
        # Fill form
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_btn.click()
        
        # Wait for redirect
        wait.until(EC.url_changes(f'{BASE_URL}/login/'))
    
    @staticmethod
    def logout(driver, wait):
        """
        Perform logout operation
        
        Args:
            driver: WebDriver instance
            wait: WebDriverWait instance
        """
        logout_btn = driver.find_element(By.LINK_TEXT, 'Logout')
        logout_btn.click()
        
        wait.until(EC.presence_of_element_located((By.ID, 'login-form')))
    
    @staticmethod
    def fill_form(driver, form_data):
        """
        Fill form with provided data
        
        Args:
            driver: WebDriver instance
            form_data: Dict with field name/id and values
        """
        for field_name, value in form_data.items():
            element = driver.find_element(By.NAME, field_name)
            element.clear()
            element.send_keys(value)
    
    @staticmethod
    def wait_for_element(wait, locator):
        """
        Wait for element to be present and clickable
        
        Args:
            wait: WebDriverWait instance
            locator: Tuple of (By.*, locator_string)
        
        Returns:
            WebElement when ready
        """
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def get_alert_message(driver, wait):
        """
        Get alert/message text from page
        
        Args:
            driver: WebDriver instance
            wait: WebDriverWait instance
        
        Returns:
            Alert message text
        """
        alert_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.alert'))
        )
        return alert_element.text


@pytest.fixture
def selenium_helper():
    """Provide SeleniumTestHelper instance"""
    return SeleniumTestHelper()
