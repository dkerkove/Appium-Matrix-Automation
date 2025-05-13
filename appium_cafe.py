from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def automate_app():
    options = XCUITestOptions()
    options.automation_name = 'XCUITest'
    
    # Unique to device
    # options.udid = '00008120B14A00BB75CCBA77' # UDID
    options.device_name = "faithful-medieval" # Name
    options.platform_name = 'iOS'
    # options.platform_version = '18.3.1' # iOS version
    
    # WDA settings
    # options.set_capability('webDriverAgentUrl', 'http://10.11.1.6:8100') # Services IP of Corellium device
    # # options.set_capability('usePreinstalledWDA', True)
    # options.set_capability('updatedWDABundleId', 'org.appium.WebDriverAgentRunner')
    # options.set_capability('updatedWDABundleIdSuffix', '.xctrunner')
    
    # App settings
    options.bundle_id = 'com.corellium.Cafe' # Bundle ID of target application
    options.set_capability('autoAcceptAlerts', True) # Automatically accepts permission requests
    
    try:
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        driver = webdriver.Remote(command_executor="https://ba1c-24-118-162-47.ngrok-free.app", options=options)
        print("Connected to Cafe app")
    
        wait = WebDriverWait(driver, 20)
    
        order_button = wait.until(EC.presence_of_element_located((AppiumBy.IOS_PREDICATE, 'label CONTAINS[c] "order"')))
        order_button.click()
        print("Starting Order")
        
        coffee_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Coffee']")))
        coffee_button.click()
        print("Coffe selected")
    
        add_to_cart_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Add to Cart']")))
        add_to_cart_button.click()
        print("Coffe Added to Cart")
    
        # try:
        #     cart_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='cart.fill']")))
        # except NoSuchElementException:
        #     cart_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Cart']")))
    
        cart_button = wait.until(EC.presence_of_element_located((AppiumBy.IOS_PREDICATE, 'label CONTAINS[c] "cart"')))
        cart_button.click()
        print("Going to Cart")
    
        promo_text_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='Promo Code']")))
        promo_text_field.send_keys("FREEJOE")
        
        apply_discount_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Apply Discount']")))
        apply_discount_button.click()
        print("Promo applied")
    
        checkout_button = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Checkout")))
        checkout_button.click()
        print("Checking out")
    
        firstname_text_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='First Name']")))
        firstname_text_field.send_keys("Myfirstname")
        lastname_text_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='Last Name']")
        lastname_text_field.send_keys("Mylastname")
        creditcard_text_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='Credit Card']")
        creditcard_text_field.send_keys("2345678901234567")
        cvv_text_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='CVV']")
        cvv_text_field.send_keys("432")
        zipcode_text_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='Zipcode']")
        zipcode_text_field.send_keys("90210")
        phone_text_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@value='Phone Number']")
        phone_text_field.send_keys("321-654-0987")
        placeorder_button = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Place Order']")
        placeorder_button.click()
        print('Order placed. Enjoy your coffee!')
    
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
    
    
    finally:
        # driver.terminate_app('com.corellium.Cafe')
        driver.quit()
