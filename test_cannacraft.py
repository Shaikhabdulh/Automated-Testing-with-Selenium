"""
Selenium Test Suite for Cannacraft Customer Feedback Website
Run: pytest test_cannacraft.py -v --html=report.html
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import sys
import socket


class TestCannacraftWebsite:
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Check if HTTP server is running (CI environment)
        if self.is_port_open('localhost', 8080):
            url = "http://localhost:8080/index.html"
            print(f"\n✅ Using HTTP server: {url}")
        else:
            # Fallback to file:// protocol for local testing
            possible_paths = [
                "index.html",
                "website.html",
                "../index.html",
                os.path.join(os.path.dirname(__file__), "index.html")
            ]
            
            file_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    file_path = os.path.abspath(path)
                    break
            
            if not file_path:
                pytest.skip("index.html not found. Please ensure the HTML file is in the repository root.")
            
            url = f"file://{file_path}"
            print(f"\n✅ Using local file: {url}")
        
        driver.get(url)
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "logo"))
            )
            print(f"✅ Page loaded successfully from: {url}")
        except TimeoutException:
            print("❌ Page failed to load within timeout")
            driver.quit()
            pytest.fail("Page did not load properly")
        
        yield driver
        driver.quit()
    
    def is_port_open(self, host, port):
        """Check if a port is open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    def wait_for_element(self, driver, by, value, timeout=10):
        """Helper method to wait for element"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            pytest.fail(f"Element not found: {by}={value}")
    
    def wait_for_clickable(self, driver, by, value, timeout=10):
        """Helper method to wait for clickable element"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except TimeoutException:
            pytest.fail(f"Element not clickable: {by}={value}")
    
    def test_page_load(self, driver):
        """Test if the page loads correctly"""
        assert "Cannacraft" in driver.title
        logo = self.wait_for_element(driver, By.CLASS_NAME, "logo")
        assert logo.text == "Cannacraft"
        print("✅ Page loaded successfully")
    
    def test_navigation_buttons_present(self, driver):
        """Test if all navigation buttons are present"""
        nav_buttons = driver.find_elements(By.CSS_SELECTOR, ".nav-links button")
        assert len(nav_buttons) == 4, f"Expected 4 buttons, found {len(nav_buttons)}"
        
        button_texts = [btn.text for btn in nav_buttons]
        assert "Home" in button_texts
        assert "Add Address" in button_texts
        assert "Book Appointment" in button_texts
        assert "Feedback" in button_texts
        print("✅ All navigation buttons present")
    
    def test_home_page_content(self, driver):
        """Test home page displays correctly"""
        home_page = driver.find_element(By.ID, "home")
        assert "active" in home_page.get_attribute("class")
        
        hero_title = driver.find_element(By.CSS_SELECTOR, ".hero h1")
        assert "Welcome to Cannacraft" in hero_title.text
        print("✅ Home page content verified")
    
    def test_navigate_to_address_page(self, driver):
        """Test navigation to Add Address page"""
        address_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(1)
        
        address_page = driver.find_element(By.ID, "address")
        assert "active" in address_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#address h2")
        assert form_title.text == "Add Address"
        print("✅ Navigated to Address page")
    
    def test_address_form_fields_present(self, driver):
        """Test all address form fields are present"""
        # Navigate to address page first
        address_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "addressForm")
        
        # Check required fields
        fields = ["firstName", "lastName", "phone", "address", "pinCode", "city", "state", "country"]
        for field in fields:
            assert form.find_element(By.NAME, field), f"Field {field} not found"
        
        print("✅ All address form fields present")
    
    def test_address_form_submission(self, driver):
        """Test address form submission with valid data"""
        # Navigate to address page
        address_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(0.5)
        
        # Fill form
        driver.find_element(By.NAME, "firstName").send_keys("John")
        driver.find_element(By.NAME, "lastName").send_keys("Doe")
        driver.find_element(By.NAME, "phone").send_keys("1234567890")
        driver.find_element(By.NAME, "address").send_keys("123 Main Street")
        driver.find_element(By.NAME, "pinCode").send_keys("12345")
        driver.find_element(By.NAME, "city").send_keys("New York")
        driver.find_element(By.NAME, "state").send_keys("NY")
        driver.find_element(By.NAME, "country").send_keys("USA")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#addressForm .btn-save")
        submit_btn.click()
        
        # Check success message
        time.sleep(1)
        success_msg = driver.find_element(By.ID, "addressSuccess")
        assert "show" in success_msg.get_attribute("class")
        assert "successfully" in success_msg.text.lower()
        print("✅ Address form submission successful")
    
    def test_address_form_validation(self, driver):
        """Test address form validation for required fields"""
        # Navigate to address page
        address_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(0.5)
        
        # Try to submit empty form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#addressForm .btn-save")
        submit_btn.click()
        
        # Check if required field validation works
        first_name = driver.find_element(By.NAME, "firstName")
        validation_message = first_name.get_attribute("validationMessage")
        assert validation_message != "", "Validation message should not be empty"
        print("✅ Form validation working")
    
    def test_navigate_to_appointment_page(self, driver):
        """Test navigation to Book Appointment page"""
        appointment_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Book Appointment']")
        appointment_btn.click()
        time.sleep(1)
        
        appointment_page = driver.find_element(By.ID, "appointment")
        assert "active" in appointment_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#appointment h2")
        assert "Schedule Your Appointment" in form_title.text
        print("✅ Navigated to Appointment page")
    
    def test_appointment_form_fields_present(self, driver):
        """Test all appointment form fields are present"""
        # Navigate to appointment page
        appointment_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Book Appointment']")
        appointment_btn.click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "appointmentForm")
        
        fields = ["firstName", "lastName", "phone", "email", "dob", "appointmentDate", "symptoms"]
        for field in fields:
            assert form.find_element(By.NAME, field), f"Field {field} not found"
        
        print("✅ All appointment form fields present")
    
    def test_appointment_form_submission(self, driver):
        """Test appointment form submission with valid data"""
        # Navigate to appointment page
        appointment_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Book Appointment']")
        appointment_btn.click()
        time.sleep(0.5)
        
        # Fill form
        driver.find_element(By.NAME, "firstName").send_keys("Jane")
        driver.find_element(By.NAME, "lastName").send_keys("Smith")
        driver.find_element(By.NAME, "phone").send_keys("9876543210")
        driver.find_element(By.NAME, "email").send_keys("jane@example.com")
        driver.find_element(By.NAME, "dob").send_keys("01011990")
        driver.find_element(By.NAME, "appointmentDate").send_keys("12312025")
        driver.find_element(By.NAME, "symptoms").send_keys("Regular checkup")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#appointmentForm .btn-save")
        submit_btn.click()
        
        # Check success message
        time.sleep(1)
        success_msg = driver.find_element(By.ID, "appointmentSuccess")
        assert "show" in success_msg.get_attribute("class")
        print("✅ Appointment form submission successful")
    
    def test_navigate_to_feedback_page(self, driver):
        """Test navigation to Feedback page"""
        feedback_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(1)
        
        feedback_page = driver.find_element(By.ID, "feedback")
        assert "active" in feedback_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#feedback h2")
        assert form_title.text == "Customer Feedback"
        print("✅ Navigated to Feedback page")
    
    def test_feedback_form_fields_present(self, driver):
        """Test all feedback form fields are present"""
        # Navigate to feedback page
        feedback_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "feedbackForm")
        
        fields = ["name", "email", "rating", "feedback"]
        for field in fields:
            assert form.find_element(By.NAME, field), f"Field {field} not found"
        
        print("✅ All feedback form fields present")
    
    def test_star_rating_system(self, driver):
        """Test star rating interaction"""
        # Navigate to feedback page
        feedback_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(0.5)
        
        # Click on 4th star
        stars = driver.find_elements(By.CLASS_NAME, "star")
        assert len(stars) == 5, f"Expected 5 stars, found {len(stars)}"
        
        # Use JavaScript click for more reliability
        driver.execute_script("arguments[0].click();", stars[3])
        time.sleep(0.5)
        
        # Check if rating value is set
        rating_value = driver.find_element(By.ID, "ratingValue")
        assert rating_value.get_attribute("value") == "4"
        
        # Check if stars are activated
        active_stars = driver.find_elements(By.CSS_SELECTOR, ".star.active")
        assert len(active_stars) == 4
        print("✅ Star rating system working")
    
    def test_feedback_form_submission(self, driver):
        """Test feedback form submission with valid data"""
        # Navigate to feedback page
        feedback_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(0.5)
        
        # Fill form
        driver.find_element(By.NAME, "name").send_keys("Alex Johnson")
        driver.find_element(By.NAME, "email").send_keys("alex@example.com")
        
        # Select rating using JavaScript
        stars = driver.find_elements(By.CLASS_NAME, "star")
        driver.execute_script("arguments[0].click();", stars[4])
        time.sleep(0.5)
        
        driver.find_element(By.NAME, "feedback").send_keys("Excellent service!")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#feedbackForm .btn-save")
        submit_btn.click()
        
        # Check success message
        time.sleep(1)
        success_msg = driver.find_element(By.ID, "feedbackSuccess")
        assert "show" in success_msg.get_attribute("class")
        assert "Thank you" in success_msg.text
        print("✅ Feedback form submission successful")
    
    def test_feedback_form_validation(self, driver):
        """Test feedback form requires rating"""
        # Navigate to feedback page
        feedback_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(0.5)
        
        # Fill only name, email, and feedback (no rating)
        driver.find_element(By.NAME, "name").send_keys("Test User")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "feedback").send_keys("Test feedback")
        
        # Try to submit without rating
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#feedbackForm .btn-save")
        submit_btn.click()
        
        # Check if rating field validation works
        rating_field = driver.find_element(By.ID, "ratingValue")
        validation_message = rating_field.get_attribute("validationMessage")
        assert validation_message != "", "Rating validation should trigger"
        print("✅ Feedback form validation working")
    
    def test_form_cancel_button(self, driver):
        """Test cancel button resets form"""
        # Navigate to address page
        address_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(0.5)
        
        # Fill some fields
        driver.find_element(By.NAME, "firstName").send_keys("Test")
        driver.find_element(By.NAME, "phone").send_keys("1234567890")
        
        # Click cancel
        cancel_btn = driver.find_element(By.CSS_SELECTOR, "#addressForm .btn-cancel")
        cancel_btn.click()
        time.sleep(0.5)
        
        # Check if form is reset
        first_name = driver.find_element(By.NAME, "firstName")
        assert first_name.get_attribute("value") == ""
        print("✅ Cancel button working")
    
    def test_hero_button_navigation(self, driver):
        """Test hero button navigates to appointment page"""
        # Navigate to home page first
        home_btn = self.wait_for_clickable(driver, By.XPATH, "//button[text()='Home']")
        home_btn.click()
        time.sleep(0.5)
        
        # Click hero button
        hero_btn = self.wait_for_clickable(driver, By.CLASS_NAME, "hero-btn")
        hero_btn.click()
        time.sleep(1)
        
        appointment_page = driver.find_element(By.ID, "appointment")
        assert "active" in appointment_page.get_attribute("class")
        print("✅ Hero button navigation working")
    
    def test_responsive_elements(self, driver):
        """Test responsive design elements are present"""
        nav = driver.find_element(By.CLASS_NAME, "nav")
        assert nav.is_displayed()
        
        container = driver.find_element(By.CLASS_NAME, "container")
        assert container.is_displayed()
        print("✅ Responsive elements present")
    
    def test_all_pages_accessibility(self, driver):
        """Test all pages can be accessed and displayed"""
        pages = {
            "home": "Home",
            "address": "Add Address",
            "appointment": "Book Appointment",
            "feedback": "Feedback"
        }
        
        for page_id, btn_text in pages.items():
            # Navigate to page
            button = self.wait_for_clickable(driver, By.XPATH, f"//button[text()='{btn_text}']")
            button.click()
            time.sleep(0.5)
            
            # Verify page is active
            page = driver.find_element(By.ID, page_id)
            assert "active" in page.get_attribute("class"), f"{page_id} page should be active"
        
        print("✅ All pages accessible")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html", "-s"])