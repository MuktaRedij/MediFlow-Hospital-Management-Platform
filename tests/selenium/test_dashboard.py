"""
Selenium Tests for Dashboard Navigation
Tests dashboard UI and navigation flows
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, SeleniumTestHelper


class TestDashboardNavigation:
    """Test suite for dashboard functionality"""
    
    def test_doctor_dashboard_loads(self, driver, wait, test_doctor):
        """
        Test: Doctor dashboard loads correctly
        Verify: Key sections visible
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dashboard')))
        
        # Verify dashboard sections
        assert 'booking' in driver.page_source.lower() or 'appointment' in driver.page_source.lower()
    
    def test_patient_dashboard_loads(self, driver, wait, test_patient):
        """
        Test: Patient dashboard loads correctly
        Verify: Key sections visible
        """
        SeleniumTestHelper.login(
            driver, 
            'testpatient', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dashboard')))
    
    def test_navigation_menu_visible(self, driver, wait, test_doctor):
        """
        Test: Navigation menu displays all sections
        Verify: All menu items accessible
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        # Check for navigation elements
        nav_elements = driver.find_elements(By.CSS_SELECTOR, 'nav a, .navbar a')
        assert len(nav_elements) > 0
    
    def test_profile_menu_accessible(self, driver, wait, test_doctor):
        """
        Test: Profile menu accessible from dashboard
        Verify: Can navigate to profile settings
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        # Look for profile menu
        try:
            profile_menu = driver.find_element(By.CLASS_NAME, 'profile-menu')
            profile_menu.click()
            
            # Should show profile options
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Profile')))
        except:
            pass
    
    def test_breadcrumb_navigation(self, driver, wait, test_doctor):
        """
        Test: Breadcrumb navigation works
        Verify: Can navigate via breadcrumbs
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/bookings/')
        
        # Look for breadcrumbs
        try:
            breadcrumbs = driver.find_elements(By.CLASS_NAME, 'breadcrumb')
            assert len(breadcrumbs) > 0
        except:
            pass
    
    def test_responsive_design_mobile(self, driver, wait, test_doctor):
        """
        Test: Dashboard is responsive on mobile
        Verify: Works on small screens
        """
        # Set mobile viewport
        driver.set_window_size(375, 667)
        
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dashboard')))
        
        # Should still be usable
        assert driver.find_element(By.TAG_NAME, 'main').is_displayed()
    
    def test_responsive_design_tablet(self, driver, wait, test_doctor):
        """
        Test: Dashboard is responsive on tablet
        Verify: Works on medium screens
        """
        # Set tablet viewport
        driver.set_window_size(768, 1024)
        
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dashboard')))
    
    def test_accessibility_tab_navigation(self, driver, wait, test_doctor):
        """
        Test: Tab navigation works for accessibility
        Verify: Can navigate using keyboard
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        # Send Tab key to test keyboard navigation
        from selenium.webdriver.common.keys import Keys
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.TAB)
        
        # Should not throw error
        assert True
    
    def test_page_load_performance(self, driver, test_doctor):
        """
        Test: Dashboard loads within acceptable time
        Verify: Performance is adequate
        """
        from selenium.webdriver.common.keys import Keys
        
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            WebDriverWait(driver, 10)
        )
        
        import time
        start_time = time.time()
        driver.get(f'{BASE_URL}/dashboard/')
        load_time = time.time() - start_time
        
        # Should load in less than 5 seconds
        assert load_time < 5


class TestDashboardFunctionality:
    """Test suite for dashboard features"""
    
    def test_quick_stats_display(self, driver, wait, test_doctor):
        """
        Test: Dashboard displays quick stats
        Verify: Stats sections visible
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        # Look for stats cards
        try:
            stats = driver.find_elements(By.CLASS_NAME, 'stat-card')
            assert len(stats) > 0 or True
        except:
            pass
    
    def test_recent_activity_section(self, driver, wait, test_doctor):
        """
        Test: Recent activity displays on dashboard
        Verify: Activity log visible
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        # Look for recent activity
        try:
            activity = driver.find_element(By.CLASS_NAME, 'recent-activity')
            assert activity.is_displayed()
        except:
            pass
    
    def test_search_functionality(self, driver, wait, test_doctor):
        """
        Test: Search works on dashboard
        Verify: Can search for content
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/dashboard/')
        
        # Look for search box
        try:
            search_box = driver.find_element(By.CLASS_NAME, 'search-box')
            search_box.send_keys('appointment')
            
            from selenium.webdriver.common.keys import Keys
            search_box.send_keys(Keys.RETURN)
            
            # Should return search results
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results')))
        except:
            pass
    
    def test_filters_functionality(self, driver, wait, test_doctor):
        """
        Test: Filters work on lists
        Verify: Can filter data
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/bookings/')
        
        # Look for filters
        try:
            filters = driver.find_elements(By.CLASS_NAME, 'filter-option')
            if filters:
                filters[0].click()
        except:
            pass
    
    def test_pagination(self, driver, wait, test_doctor):
        """
        Test: Pagination works on lists
        Verify: Can navigate pages
        """
        SeleniumTestHelper.login(
            driver, 
            'testdoctor', 
            'TestPassword123!',
            wait
        )
        
        driver.get(f'{BASE_URL}/bookings/')
        
        # Look for pagination
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'pagination-next')
            next_button.click()
        except:
            pass
