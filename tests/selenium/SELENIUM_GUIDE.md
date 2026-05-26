# Selenium Test Execution Guide
## Running Browser Automation Tests for MediFlow

This guide covers running, debugging, and maintaining Selenium tests.

## Setup

### Install Dependencies

```bash
# Navigate to project root
cd /path/to/mediflow

# Install Python dependencies
pip install -r requirements.txt
pip install selenium==4.15.2
pip install pytest==7.4.3
pip install pytest-django==4.7.0
pip install coverage==7.3.2

# Install ChromeDriver
# Option 1: Using webdriver-manager (automatic)
pip install webdriver-manager

# Option 2: Manual installation
wget https://chromedriver.chromium.org/downloads
# Extract and add to PATH
```

## Running Tests

### Run All Selenium Tests

```bash
# Basic execution
pytest tests/selenium/ -v

# With coverage report
pytest tests/selenium/ -v --cov=tests/selenium

# Generate HTML report
pytest tests/selenium/ -v \
  --html=report.html \
  --self-contained-html
```

### Run Specific Test File

```bash
# Login tests
pytest tests/selenium/test_login.py -v

# Booking tests
pytest tests/selenium/test_booking.py -v

# Dashboard tests
pytest tests/selenium/test_dashboard.py -v
```

### Run Specific Test

```bash
# Single test method
pytest tests/selenium/test_login.py::TestLoginFlow::test_doctor_login_success -v

# With keyword matching
pytest tests/selenium/ -k "test_login" -v

# With marker (custom markers)
pytest tests/selenium/ -m "smoke" -v
```

## Browser Configuration

### Headless Mode

```bash
# Run in headless mode (no GUI)
HEADLESS_BROWSER=true pytest tests/selenium/ -v

# Useful for CI/CD pipelines
```

### Headful Mode (Debug)

```bash
# Run with browser visible
HEADLESS_BROWSER=false pytest tests/selenium/ -v

# Good for visual debugging
```

### Custom Viewport

```python
# Modify conftest.py chrome_options
options.add_argument('--window-size=1920,1080')

# Mobile viewport
options.add_argument('--window-size=375,667')

# Tablet viewport
options.add_argument('--window-size=768,1024')
```

## Test Organization

### Login Tests (`test_login.py`)

**TestLoginFlow class:**
- `test_login_page_loads` - Verify login page displays
- `test_doctor_login_success` - Doctor login workflow
- `test_patient_login_success` - Patient login workflow
- `test_invalid_credentials` - Error handling
- `test_empty_username_validation` - Form validation
- `test_password_field_masked` - Security check
- `test_session_persistence` - Session management
- `test_logout_functionality` - Logout workflow
- `test_remember_me_functionality` - Optional feature
- `test_form_submission_via_enter_key` - Keyboard shortcut

**TestSignupFlow class:**
- `test_doctor_signup_page_loads` - Doctor signup form
- `test_patient_signup_page_loads` - Patient signup form

### Booking Tests (`test_booking.py`)

**TestAppointmentBooking class:**
- `test_doctor_list_page_loads` - Doctor listing
- `test_doctor_availability_slots_display` - View availability
- `test_booking_form_validation` - Form validation
- `test_select_appointment_time` - Time slot selection
- `test_booking_confirmation_message` - Confirmation display
- `test_prevent_double_booking` - Concurrency control
- `test_booking_cancellation` - Cancel booking
- `test_booking_reschedule` - Reschedule booking

**TestAvailabilityManagement class:**
- `test_doctor_can_view_bookings` - Doctor booking list
- `test_doctor_can_create_availability` - Create slots
- `test_availability_date_validation` - Date validation

**TestFormValidation class:**
- `test_email_format_validation` - Email validation
- `test_password_strength_validation` - Password rules
- `test_required_field_highlighting` - Required fields

### Dashboard Tests (`test_dashboard.py`)

**TestDashboardNavigation class:**
- `test_doctor_dashboard_loads` - Doctor dashboard
- `test_patient_dashboard_loads` - Patient dashboard
- `test_navigation_menu_visible` - Navigation menu
- `test_profile_menu_accessible` - Profile menu
- `test_breadcrumb_navigation` - Breadcrumbs
- `test_responsive_design_mobile` - Mobile responsiveness
- `test_responsive_design_tablet` - Tablet responsiveness
- `test_accessibility_tab_navigation` - Keyboard navigation
- `test_page_load_performance` - Load time < 5s

**TestDashboardFunctionality class:**
- `test_quick_stats_display` - Stats cards
- `test_recent_activity_section` - Activity log
- `test_search_functionality` - Search feature
- `test_filters_functionality` - Filter options
- `test_pagination` - Pagination navigation

## Debugging Tests

### Verbose Output

```bash
# Show full output
pytest tests/selenium/test_login.py -vv -s

# Show print statements
pytest tests/selenium/ -s
```

### Stop on First Failure

```bash
pytest tests/selenium/ -x  # Stop on first failure
pytest tests/selenium/ -x -v  # Verbose + stop
```

### Interactive Debug Mode

```bash
# Drop to debugger on failure
pytest tests/selenium/ --pdb

# Drop on failures and errors
pytest tests/selenium/ --pdb-trace
```

### Screenshots on Failure

```python
# Add to test
@pytest.fixture(autouse=True)
def capture_screenshot(driver, request):
    yield
    if request.node.rep_call.failed:
        driver.save_screenshot(f"screenshots/{request.node.name}.png")
```

### Slow Motion (See actions)

```python
# Modify WebDriver
driver.set_script_timeout(10)  # Longer script timeout

# Or manually add delays
time.sleep(1)  # Add pause between actions
```

## CI/CD Integration

### Jenkins Integration

```bash
# Run tests in Jenkins Jenkinsfile
stage('Selenium Integration Tests') {
    steps {
        sh '''
            . ${VENV_PATH}/bin/activate
            python -m pytest tests/selenium/ -v \
              --junit=test-results.xml \
              --html=test-report.html
        '''
    }
    post {
        always {
            junit 'test-results.xml'
            publishHTML(target: [
                reportDir: '.',
                reportFiles: 'test-report.html',
                reportName: 'Selenium Tests'
            ])
        }
    }
}
```

### GitHub Actions Integration

```yaml
# .github/workflows/tests.yml
name: Selenium Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/selenium/ -v --html=report.html
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-report
          path: report.html
```

## Test Reports

### Generate HTML Report

```bash
pytest tests/selenium/ --html=report.html --self-contained-html
```

### Generate XML Report (for CI)

```bash
pytest tests/selenium/ --junit=results.xml
```

### Coverage Report

```bash
# Generate coverage
pytest tests/selenium/ --cov=tests/selenium --cov-report=html

# View report
open htmlcov/index.html
```

## Best Practices

### Test Independence
- Each test should be independent
- No shared state between tests
- Clean up after each test

### Waits
- Use explicit waits (not implicit)
- Wait for specific conditions
- Set reasonable timeout values

### Page Objects
- Organize selectors in helper classes
- Use SeleniumTestHelper utility
- Keep selectors DRY

### Error Handling
- Handle exceptions gracefully
- Provide meaningful error messages
- Take screenshots on failure

### Maintenance
- Update tests when UI changes
- Keep test data current
- Review and refactor regularly
- Document complex tests

## Troubleshooting

### ChromeDriver Version Mismatch

```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Or download matching version
# https://chromedriver.chromium.org/
```

### Element Not Found

```python
# Increase timeout
wait = WebDriverWait(driver, 20)

# Debug selector
elements = driver.find_elements(By.CSS_SELECTOR, '.selector')
print(f"Found {len(elements)} elements")
```

### Stale Element Reference

```python
# Re-find element in loop
for i in range(3):
    try:
        element = driver.find_element(By.ID, 'button')
        element.click()
        break
    except StaleElementReferenceException:
        continue
```

### Timeout Issues

```bash
# Increase timeout for slow environments
TEST_TIMEOUT=30 pytest tests/selenium/

# Or in conftest.py
TIMEOUT = 30  # seconds
```

## Performance Testing

### Measure Load Time

```python
import time

start = time.time()
driver.get(url)
load_time = time.time() - start
assert load_time < 5.0, f"Page too slow: {load_time}s"
```

### Monitor Resources

```bash
# Run with resource monitoring
pytest tests/selenium/ --durations=10
```

---

For more information, see [conftest.py](../conftest.py) and test files.
