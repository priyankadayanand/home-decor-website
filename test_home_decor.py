from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import time
import os

class TestHomeDecorLandingPage:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--headless=new")  # Updated headless mode
            
            # Setup Chrome driver with explicit executable path
            driver_path = ChromeDriverManager().install()
            service = Service(executable_path=driver_path)
            
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            
            # Start local server
            os.system('start python -m http.server 8000')
            time.sleep(2)  # Wait for server to start
            
            yield
            
        except Exception as e:
            print(f"Setup error: {str(e)}")
            raise e
        
        finally:
            # Cleanup
            if hasattr(self, 'driver'):
                self.driver.quit()
            os.system("taskkill /f /im python.exe")  # Stop the server

    def test_landing_page_elements(self):
        """Test the presence and functionality of landing page elements"""
        self.driver.get("http://localhost:8000")  # Replace with your actual URL

        # Test Header Navigation
        header = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        assert header.is_displayed(), "Header is not visible"

        # Test Logo
        logo = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
        assert logo.is_displayed(), "Logo is not visible"

        # Test Navigation Links
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, ".nav-links a")
        expected_links = ["Home", "Products", "Collections", "About", "Contact"]
        actual_links = [link.text for link in nav_links]
        assert actual_links == expected_links, f"Navigation links don't match. Expected: {expected_links}, Got: {actual_links}"

    def test_hero_section(self):
        """Test the hero section content and CTA button"""
        self.driver.get("http://localhost:8000")

        # Test Hero Title
        hero_title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".hero h1")))
        assert "Transform Your Space" in hero_title.text, "Hero title not found or incorrect"

        # Test CTA Button
        cta_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cta-button")))
        assert cta_button.is_displayed(), "CTA button not visible"
        assert "Shop Now" in cta_button.text, "CTA button text incorrect"

    def test_featured_products(self):
        """Test the featured products section"""
        self.driver.get("http://localhost:8000")

        # Test Products Section
        products_section = self.wait.until(EC.presence_of_element_located((By.ID, "featured-products")))
        assert products_section.is_displayed(), "Featured products section not visible"

        # Test Product Cards
        product_cards = self.driver.find_elements(By.CLASS_NAME, "product-card")
        assert len(product_cards) > 0, "No product cards found"

        # Test First Product Card
        first_product = product_cards[0]
        assert first_product.find_element(By.TAG_NAME, "img").is_displayed(), "Product image not visible"
        assert first_product.find_element(By.CLASS_NAME, "product-title").text != "", "Product title is empty"
        assert first_product.find_element(By.CLASS_NAME, "product-price").text != "", "Product price is empty"

    def test_search_functionality(self):
        """Test the search functionality"""
        self.driver.get("http://localhost:8000")

        # Test Search Input
        search_input = self.wait.until(EC.presence_of_element_located((By.ID, "search-input")))
        search_button = self.wait.until(EC.element_to_be_clickable((By.ID, "search-button")))

        # Enter search term
        search_input.send_keys("Modern Sofa")
        search_button.click()

        # Wait for search results
        search_results = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
        assert search_results.is_displayed(), "Search results not displayed"

    def test_newsletter_signup(self):
        """Test the newsletter signup functionality"""
        self.driver.get("http://localhost:8000")

        # Scroll to newsletter section
        newsletter_section = self.wait.until(EC.presence_of_element_located((By.ID, "newsletter")))
        self.driver.execute_script("arguments[0].scrollIntoView();", newsletter_section)

        # Test Email Input
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "newsletter-email")))
        submit_button = self.wait.until(EC.element_to_be_clickable((By.ID, "newsletter-submit")))

        # Enter email and submit
        test_email = "test@example.com"
        email_input.send_keys(test_email)
        submit_button.click()

        # Check success message
        success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
        assert success_message.is_displayed(), "Success message not displayed"
        assert "Thank you for subscribing" in success_message.text, "Incorrect success message"

    def test_responsive_design(self):
        """Test responsive design at different screen sizes"""
        self.driver.get("http://localhost:8000")

        # Test mobile view
        self.driver.set_window_size(375, 812)  # iPhone X dimensions
        time.sleep(1)  # Wait for responsive changes
        
        # Check hamburger menu
        hamburger_menu = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hamburger-menu")))
        assert hamburger_menu.is_displayed(), "Hamburger menu not visible on mobile"

        # Test tablet view
        self.driver.set_window_size(768, 1024)  # iPad dimensions
        time.sleep(1)

        # Test desktop view
        self.driver.set_window_size(1920, 1080)  # Full HD
        time.sleep(1)

        # Verify navigation is visible on desktop
        nav_menu = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-links")))
        assert nav_menu.is_displayed(), "Navigation menu not visible on desktop" 