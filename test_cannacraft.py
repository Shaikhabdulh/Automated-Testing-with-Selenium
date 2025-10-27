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
from selenium.common.exceptions import TimeoutException
import time
import os


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
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Load the HTML file
        file_path = os.path.abspath("index.html")
        driver.get(f"file://{file_path}")
        
        yield driver
        driver.quit()
    
    def wait_for_element(self, driver, by, value, timeout=10):
        """Helper method to wait for element"""
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def test_page_load(self, driver):
        """Test if the page loads correctly"""
        assert "Cannacraft" in driver.title
        logo = driver.find_element(By.CLASS_NAME, "logo")
        assert logo.text == "Cannacraft"
    
    def test_navigation_buttons_present(self, driver):
        """Test if all navigation buttons are present"""
        nav_buttons = driver.find_elements(By.CSS_SELECTOR, ".nav-links button")
        assert len(nav_buttons) == 4
        
        button_texts = [btn.text for btn in nav_buttons]
        assert "Home" in button_texts
        assert "Add Address" in button_texts
        assert "Book Appointment" in button_texts
        assert "Feedback" in button_texts
    
    def test_home_page_content(self, driver):
        """Test home page displays correctly"""
        home_page = driver.find_element(By.ID, "home")
        assert home_page.is_displayed()
        
        hero_title = driver.find_element(By.CSS_SELECTOR, ".hero h1")
        assert "Welcome to Cannacraft" in hero_title.text
    
    def test_navigate_to_address_page(self, driver):
        """Test navigation to Add Address page"""
        address_btn = driver.find_element(By.XPATH, "//button[text()='Add Address']")
        address_btn.click()
        time.sleep(0.5)
        
        address_page = driver.find_element(By.ID, "address")
        assert "active" in address_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#address h2")
        assert form_title.text == "Add Address"
    
    def test_address_form_fields_present(self, driver):
        """Test all address form fields are present"""
        driver.find_element(By.XPATH, "//button[text()='Add Address']").click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "addressForm")
        
        # Check required fields
        assert form.find_element(By.NAME, "firstName")
        assert form.find_element(By.NAME, "lastName")
        assert form.find_element(By.NAME, "phone")
        assert form.find_element(By.NAME, "address")
        assert form.find_element(By.NAME, "pinCode")
        assert form.find_element(By.NAME, "city")
        assert form.find_element(By.NAME, "state")
        assert form.find_element(By.NAME, "country")
    
    def test_address_form_submission(self, driver):
        """Test address form submission with valid data"""
        driver.find_element(By.XPATH, "//button[text()='Add Address']").click()
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
        time.sleep(0.5)
        success_msg = driver.find_element(By.ID, "addressSuccess")
        assert "show" in success_msg.get_attribute("class")
        assert "successfully" in success_msg.text.lower()
    
    def test_address_form_validation(self, driver):
        """Test address form validation for required fields"""
        driver.find_element(By.XPATH, "//button[text()='Add Address']").click()
        time.sleep(0.5)
        
        # Try to submit empty form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#addressForm .btn-save")
        submit_btn.click()
        
        # Check if required field validation works
        first_name = driver.find_element(By.NAME, "firstName")
        validation_message = first_name.get_attribute("validationMessage")
        assert validation_message != ""
    
    def test_navigate_to_appointment_page(self, driver):
        """Test navigation to Book Appointment page"""
        appointment_btn = driver.find_element(By.XPATH, "//button[text()='Book Appointment']")
        appointment_btn.click()
        time.sleep(0.5)
        
        appointment_page = driver.find_element(By.ID, "appointment")
        assert "active" in appointment_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#appointment h2")
        assert "Schedule Your Appointment" in form_title.text
    
    def test_appointment_form_fields_present(self, driver):
        """Test all appointment form fields are present"""
        driver.find_element(By.XPATH, "//button[text()='Book Appointment']").click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "appointmentForm")
        
        assert form.find_element(By.NAME, "firstName")
        assert form.find_element(By.NAME, "lastName")
        assert form.find_element(By.NAME, "phone")
        assert form.find_element(By.NAME, "email")
        assert form.find_element(By.NAME, "dob")
        assert form.find_element(By.NAME, "appointmentDate")
        assert form.find_element(By.NAME, "symptoms")
    
    def test_appointment_form_submission(self, driver):
        """Test appointment form submission with valid data"""
        driver.find_element(By.XPATH, "//button[text()='Book Appointment']").click()
        time.sleep(0.5)
        
        # Fill form
        driver.find_element(By.NAME, "firstName").send_keys("Jane")
        driver.find_element(By.NAME, "lastName").send_keys("Smith")
        driver.find_element(By.NAME, "phone").send_keys("9876543210")
        driver.find_element(By.NAME, "email").send_keys("jane@example.com")
        driver.find_element(By.NAME, "dob").send_keys("01/01/1990")
        driver.find_element(By.NAME, "appointmentDate").send_keys("12/31/2025")
        driver.find_element(By.NAME, "symptoms").send_keys("Regular checkup")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#appointmentForm .btn-save")
        submit_btn.click()
        
        # Check success message
        time.sleep(0.5)
        success_msg = driver.find_element(By.ID, "appointmentSuccess")
        assert "show" in success_msg.get_attribute("class")
    
    def test_navigate_to_feedback_page(self, driver):
        """Test navigation to Feedback page"""
        feedback_btn = driver.find_element(By.XPATH, "//button[text()='Feedback']")
        feedback_btn.click()
        time.sleep(0.5)
        
        feedback_page = driver.find_element(By.ID, "feedback")
        assert "active" in feedback_page.get_attribute("class")
        
        form_title = driver.find_element(By.CSS_SELECTOR, "#feedback h2")
        assert form_title.text == "Customer Feedback"
    
    def test_feedback_form_fields_present(self, driver):
        """Test all feedback form fields are present"""
        driver.find_element(By.XPATH, "//button[text()='Feedback']").click()
        time.sleep(0.5)
        
        form = driver.find_element(By.ID, "feedbackForm")
        
        assert form.find_element(By.NAME, "name")
        assert form.find_element(By.NAME, "email")
        assert form.find_element(By.NAME, "rating")
        assert form.find_element(By.NAME, "feedback")
    
    def test_star_rating_system(self, driver):
        """Test star rating interaction"""
        driver.find_element(By.XPATH, "//button[text()='Feedback']").click()
        time.sleep(0.5)
        
        # Click on 4th star
        stars = driver.find_elements(By.CLASS_NAME, "star")
        assert len(stars) == 5
        
        stars[3].click()  # Click 4th star (index 3)
        time.sleep(0.3)
        
        # Check if rating value is set
        rating_value = driver.find_element(By.ID, "ratingValue")
        assert rating_value.get_attribute("value") == "4"
        
        # Check if stars are activated
        active_stars = driver.find_elements(By.CSS_SELECTOR, ".star.active")
        assert len(active_stars) == 4
    
    def test_feedback_form_submission(self, driver):
        """Test feedback form submission with valid data"""
        driver.find_element(By.XPATH, "//button[text()='Feedback']").click()
        time.sleep(0.5)
        
        # Fill form
        driver.find_element(By.NAME, "name").send_keys("Alex Johnson")
        driver.find_element(By.NAME, "email").send_keys("alex@example.com")
        
        # Select rating
        stars = driver.find_elements(By.CLASS_NAME, "star")
        stars[4].click()  # 5 stars
        time.sleep(0.3)
        
        driver.find_element(By.NAME, "feedback").send_keys("Excellent service!")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#feedbackForm .btn-save")
        submit_btn.click()
        
        # Check success message
        time.sleep(0.5)
        success_msg = driver.find_element(By.ID, "feedbackSuccess")
        assert "show" in success_msg.get_attribute("class")
        assert "Thank you" in success_msg.text
    
    def test_feedback_form_validation(self, driver):
        """Test feedback form requires rating"""
        driver.find_element(By.XPATH, "//button[text()='Feedback']").click()
        time.sleep(0.5)
        
        # Fill only name and email
        driver.find_element(By.NAME, "name").send_keys("Test User")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "feedback").send_keys("Test feedback")
        
        # Try to submit without rating
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#feedbackForm .btn-save")
        submit_btn.click()
        
        # Check if rating field validation works
        rating_field = driver.find_element(By.ID, "ratingValue")
        validation_message = rating_field.get_attribute("validationMessage")
        assert validation_message != ""
    
    def test_form_cancel_button(self, driver):
        """Test cancel button resets form"""
        driver.find_element(By.XPATH, "//button[text()='Add Address']").click()
        time.sleep(0.5)
        
        # Fill some fields
        driver.find_element(By.NAME, "firstName").send_keys("Test")
        driver.find_element(By.NAME, "phone").send_keys("1234567890")
        
        # Click cancel
        cancel_btn = driver.find_element(By.CSS_SELECTOR, "#addressForm .btn-cancel")
        cancel_btn.click()
        time.sleep(0.3)
        
        # Check if form is reset
        first_name = driver.find_element(By.NAME, "firstName")
        assert first_name.get_attribute("value") == ""
    
    def test_hero_button_navigation(self, driver):
        """Test hero button navigates to appointment page"""
        driver.find_element(By.XPATH, "//button[text()='Home']").click()
        time.sleep(0.5)
        
        hero_btn = driver.find_element(By.CLASS_NAME, "hero-btn")
        hero_btn.click()
        time.sleep(0.5)
        
        appointment_page = driver.find_element(By.ID, "appointment")
        assert "active" in appointment_page.get_attribute("class")
    
    def test_responsive_elements(self, driver):
        """Test responsive design elements are present"""
        # Test that key elements exist
        nav = driver.find_element(By.CLASS_NAME, "nav")
        assert nav.is_displayed()
        
        container = driver.find_element(By.CLASS_NAME, "container")
        assert container.is_displayed()
    
    def test_all_pages_accessibility(self, driver):
        """Test all pages can be accessed and displayed"""
        pages = ["home", "address", "appointment", "feedback"]
        
        for page_id in pages:
            # Navigate to page
            if page_id == "home":
                btn_text = "Home"
            elif page_id == "address":
                btn_text = "Add Address"
            elif page_id == "appointment":
                btn_text = "Book Appointment"
            else:
                btn_text = "Feedback"
            
            driver.find_element(By.XPATH, f"//button[text()='{btn_text}']").click()
            time.sleep(0.5)
            
            # Verify page is active
            page = driver.find_element(By.ID, page_id)
            assert "active" in page.get_attribute("class"), f"{page_id} page should be active"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])