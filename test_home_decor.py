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

class TestHomeDecorWebsite:
    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--headless=new")
            
            # Setup Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            
            # Start local server
            os.system('start python -m http.server 8000')
            time.sleep(2)  # Wait for server to start
            
            yield
            
        finally:
            if hasattr(self, 'driver'):
                self.driver.quit()
            os.system("taskkill /f /im python.exe")

    def test_header_navigation(self):
        """Test header navigation elements"""
        self.driver.get("http://localhost:8000")
        
        # Test logo
        logo = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
        assert logo.text == "Elegant Living"
        assert logo.is_displayed()
        
        # Test navigation links
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, ".nav-links a")
        expected_links = ["Home", "Categories", "Products", "About", "Contact"]
        actual_links = [link.text for link in nav_links]
        assert actual_links == expected_links
        
        # Test cart icon
        cart_icon = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-icon")))
        assert cart_icon.is_displayed()

    def test_hero_section(self):
        """Test hero section content"""
        self.driver.get("http://localhost:8000")
        
        # Test hero title
        hero_title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".hero h1")))
        assert hero_title.text == "Transform Your Space"
        
        # Test hero description
        hero_desc = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".hero p")))
        assert "Discover unique pieces" in hero_desc.text
        
        # Test CTA button
        cta_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cta-button")))
        assert cta_button.text == "Shop Collection"
        assert cta_button.is_displayed()

    def test_featured_categories(self):
        """Test featured categories section"""
        self.driver.get("http://localhost:8000")
        
        # Test section title
        section_title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#categories .section-title")))
        assert section_title.text == "Featured Categories"
        
        # Test category cards
        category_cards = self.driver.find_elements(By.CLASS_NAME, "category-card")
        assert len(category_cards) == 3
        
        # Test first category
        first_category = category_cards[0]
        assert first_category.find_element(By.TAG_NAME, "img").get_attribute("alt") == "Living Room"
        assert first_category.find_element(By.TAG_NAME, "h3").text == "Living Room"

    def test_product_gallery(self):
        """Test product gallery section"""
        self.driver.get("http://localhost:8000")
        
        # Test section title
        section_title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#products .section-title")))
        assert section_title.text == "Featured Products"
        
        # Test product cards
        product_cards = self.driver.find_elements(By.CLASS_NAME, "product-card")
        assert len(product_cards) == 4
        
        # Test first product
        first_product = product_cards[0]
        assert first_product.find_element(By.CLASS_NAME, "product-title").text == "Modern Comfort Sofa"
        assert "€799" in first_product.find_element(By.CLASS_NAME, "product-price").text

    def test_product_slideshow(self):
        """Test product slideshow functionality"""
        self.driver.get("http://localhost:8000")
        
        # Test sofa slideshow
        sofa_slideshow = self.wait.until(EC.presence_of_element_located((By.ID, "sofaSlideshow")))
        assert sofa_slideshow.is_displayed()
        
        # Test slideshow navigation dots
        slideshow_dots = sofa_slideshow.find_elements(By.CLASS_NAME, "slideshow-dot")
        assert len(slideshow_dots) == 5
        
        # Test image visibility
        active_image = sofa_slideshow.find_element(By.CSS_SELECTOR, ".slideshow-images img.active")
        assert active_image.is_displayed()

    def test_newsletter_section(self):
        """Test newsletter section"""
        self.driver.get("http://localhost:8000")
        
        # Test newsletter form
        newsletter_form = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "newsletter-form")))
        assert newsletter_form.is_displayed()
        
        # Test input field
        email_input = newsletter_form.find_element(By.TAG_NAME, "input")
        assert email_input.get_attribute("type") == "email"
        assert email_input.get_attribute("placeholder") == "Enter your email address"
        
        # Test subscribe button
        subscribe_button = newsletter_form.find_element(By.TAG_NAME, "button")
        assert subscribe_button.text == "Subscribe"

    def test_footer_content(self):
        """Test footer content"""
        self.driver.get("http://localhost:8000")
        
        # Test footer sections
        footer_sections = self.driver.find_elements(By.CLASS_NAME, "footer-section")
        assert len(footer_sections) == 4
        
        # Test footer links
        footer_links = self.driver.find_elements(By.CSS_SELECTOR, ".footer-section a")
        assert len(footer_links) > 0
        
        # Test copyright
        copyright_text = self.driver.find_element(By.CLASS_NAME, "copyright")
        assert "2024" in copyright_text.text
        assert "Elegant Living" in copyright_text.text

    def test_responsive_design(self):
        """Test responsive design at different screen sizes"""
        self.driver.get("http://localhost:8000")
        
        # Test mobile view
        self.driver.set_window_size(375, 812)  # iPhone X
        mobile_menu = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mobile-menu-btn")))
        assert mobile_menu.is_displayed()
        
        # Test tablet view
        self.driver.set_window_size(768, 1024)  # iPad
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, ".nav-links a")
        assert len(nav_links) > 0
        
        # Test desktop view
        self.driver.set_window_size(1920, 1080)
        assert not mobile_menu.is_displayed()

    def test_cart_functionality(self):
        """Test shopping cart functionality"""
        self.driver.get("http://localhost:8000")
        
        # Test cart icon
        cart_icon = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-icon")))
        cart_icon.click()
        
        # Test cart overlay
        cart_overlay = self.wait.until(EC.presence_of_element_located((By.ID, "cartOverlay")))
        assert cart_overlay.is_displayed()
        
        # Test cart total
        cart_total = cart_overlay.find_element(By.ID, "cartTotal")
        assert cart_total.text == "€0.00"
        
        # Test checkout button
        checkout_button = cart_overlay.find_element(By.CLASS_NAME, "checkout-button")
        assert checkout_button.is_displayed()
        assert checkout_button.text == "Proceed to Checkout"

    def test_add_to_cart_flow(self):
        """Test adding products to cart"""
        self.driver.get("http://localhost:8000")
        
        # Click first product to open details
        first_product = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-card")))
        first_product.click()
        
        # Wait for product lightbox
        lightbox = self.wait.until(EC.presence_of_element_located((By.ID, "productLightbox")))
        assert lightbox.is_displayed()
        
        # Get initial cart count
        cart_count = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-count")))
        initial_count = int(cart_count.text)
        
        # Add product to cart
        add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")))
        add_to_cart_btn.click()
        
        # Verify cart count increased
        updated_count = int(cart_count.text)
        assert updated_count == initial_count + 1
        
        # Verify cart overlay opened
        cart_overlay = self.wait.until(EC.presence_of_element_located((By.ID, "cartOverlay")))
        assert cart_overlay.is_displayed()
        
        # Verify product added to cart
        cart_items = cart_overlay.find_elements(By.CLASS_NAME, "cart-item")
        assert len(cart_items) == 1
        assert "Modern Comfort Sofa" in cart_items[0].text
        assert "€799" in cart_items[0].text

    def test_cart_manipulation(self):
        """Test cart item manipulation"""
        self.driver.get("http://localhost:8000")
        
        # Add two products to cart
        products = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card")))
        for product in products[:2]:
            product.click()
            add_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")))
            add_btn.click()
            time.sleep(1)  # Wait for cart update
        
        # Open cart
        cart_icon = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart-icon")))
        cart_icon.click()
        
        # Verify two items in cart
        cart_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart-item")))
        assert len(cart_items) == 2
        
        # Remove first item
        remove_btn = cart_items[0].find_element(By.CLASS_NAME, "cart-item-remove")
        remove_btn.click()
        
        # Verify item removed
        updated_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart-item")))
        assert len(updated_items) == 1
        
        # Verify cart count updated
        cart_count = self.driver.find_element(By.CLASS_NAME, "cart-count")
        assert cart_count.text == "1"

    def test_checkout_flow(self):
        """Test checkout process"""
        self.driver.get("http://localhost:8000")
        
        # Add a product to cart
        first_product = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-card")))
        first_product.click()
        add_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")))
        add_btn.click()
        
        # Click checkout button
        checkout_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-button")))
        checkout_btn.click()
        
        # Verify payment overlay displayed
        payment_overlay = self.wait.until(EC.presence_of_element_located((By.ID, "paymentOverlay")))
        assert payment_overlay.is_displayed()
        
        # Fill payment form
        self.fill_payment_form({
            "name": "John Doe",
            "email": "john@example.com",
            "card": "4242 4242 4242 4242",
            "expiry": "12/25",
            "cvv": "123"
        })
        
        # Submit payment
        pay_button = payment_overlay.find_element(By.CSS_SELECTOR, "button[type='submit']")
        pay_button.click()
        
        # Verify cart emptied
        cart_count = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-count")))
        assert cart_count.text == "0"

    def test_payment_form_validation(self):
        """Test payment form validation"""
        self.driver.get("http://localhost:8000")
        
        # Add product and go to payment
        first_product = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-card")))
        first_product.click()
        add_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")))
        add_btn.click()
        checkout_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-button")))
        checkout_btn.click()
        
        # Test empty form submission
        payment_form = self.wait.until(EC.presence_of_element_located((By.ID, "paymentForm")))
        submit_button = payment_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verify form validation
        required_fields = payment_form.find_elements(By.CSS_SELECTOR, "input:required")
        for field in required_fields:
            assert not field.get_attribute("validity").get("valid")
        
        # Test invalid email
        self.fill_payment_form({
            "name": "John Doe",
            "email": "invalid-email",
            "card": "4242 4242 4242 4242",
            "expiry": "12/25",
            "cvv": "123"
        })
        submit_button.click()
        
        email_input = payment_form.find_element(By.CSS_SELECTOR, "input[type='email']")
        assert not email_input.get_attribute("validity").get("valid")

    def test_payment_cancellation(self):
        """Test payment cancellation"""
        self.driver.get("http://localhost:8000")
        
        # Add product and go to payment
        first_product = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-card")))
        first_product.click()
        add_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")))
        add_btn.click()
        checkout_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-button")))
        checkout_btn.click()
        
        # Test cancel button
        cancel_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cancel-button")))
        cancel_button.click()
        
        # Verify payment overlay closed
        payment_overlay = self.driver.find_element(By.ID, "paymentOverlay")
        assert not payment_overlay.is_displayed()
        
        # Verify cart still has items
        cart_count = self.driver.find_element(By.CLASS_NAME, "cart-count")
        assert cart_count.text == "1"

    def fill_payment_form(self, data):
        """Helper method to fill payment form"""
        payment_form = self.wait.until(EC.presence_of_element_located((By.ID, "paymentForm")))
        
        # Fill name
        name_input = payment_form.find_element(By.CSS_SELECTOR, "input[placeholder='John Doe']")
        name_input.clear()
        name_input.send_keys(data["name"])
        
        # Fill email
        email_input = payment_form.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_input.clear()
        email_input.send_keys(data["email"])
        
        # Fill card number
        card_input = payment_form.find_element(By.CSS_SELECTOR, "input[placeholder='1234 5678 9012 3456']")
        card_input.clear()
        card_input.send_keys(data["card"])
        
        # Fill expiry
        expiry_input = payment_form.find_element(By.CSS_SELECTOR, "input[placeholder='MM/YY']")
        expiry_input.clear()
        expiry_input.send_keys(data["expiry"])
        
        # Fill CVV
        cvv_input = payment_form.find_element(By.CSS_SELECTOR, "input[placeholder='123']")
        cvv_input.clear()
        cvv_input.send_keys(data["cvv"]) 