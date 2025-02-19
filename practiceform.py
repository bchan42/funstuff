# filling out form part

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pickle
import time
import os

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # initialize chromedriver
wait = WebDriverWait(driver, 10) # wait object

# check if cookies file exists
if os.path.exists("cookies.pkl"):
    print("Loading saved cookies...")
    driver.get('https://now.calpoly.edu/')  # go to domain to match cookies

    # wait for domain to load fully before adding cookies
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # load cookies
    with open("cookies.pkl", "rb") as cookie_file:
        cookies = pickle.load(cookie_file)
        for cookie in cookies:
            # check if domain in cookie matches current domain
            if 'domain' in cookie:
                cookie['domain'] = '.calpoly.edu'
            driver.add_cookie(cookie)

    # after adding cookies, go to the desired page directly
    driver.get('https://now.calpoly.edu/actionCenter/organization/wish/Finance/CreatePurchaseRequest')  # PRF form page
    time.sleep(5)

    # wait to make sure page has loaded and that we're still on the PRF page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Create Purchase Request')]"))
        )
        print("PRF form page loaded successfully!")
    except:
        print("Failed to load PRF form. You may need to log in again.")
        time.sleep(5)

else:
    # if cookies don't exist, log in manually
    driver.get('https://now.calpoly.edu/')
    signin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))
    )
    signin_button.click()

    # manually enter login credentials and submit
    print("Please log in manually (and approve Duo).")
    time.sleep(15)  # wait for manual login and Duo approval

    # save cookies after successful login
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as cookie_file:
        pickle.dump(cookies, cookie_file)
    
    # access form
    driver.get('https://now.calpoly.edu/actionCenter/organization/wish/Finance/CreatePurchaseRequest')  # PRF form page
    time.sleep(5)

# check if you're on the form page
print("Now on the PRF form!") 


# START FILLING OUT FORM

try:

    # REQUEST DETAILS SECTION
    # subject / event name field
    subject_field = wait.until(EC.presence_of_element_located((By.NAME, "Subject")))
    subject_field.send_keys("General Meeting #1")

    # description field
    description_field = wait.until(EC.presence_of_element_located((By.NAME, "Description")))
    description_field.send_keys("3 Pepperoni Pizzas")

    # requested amount field
    requested_amount_field = wait.until(EC.presence_of_element_located((By.NAME, "RequestedAmount")))
    requested_amount_field.send_keys("100") 

    # categories dropdown (select where money comes from) (pretty much always)
    category_dropdown = wait.until(EC.presence_of_element_located((By.ID, "CategoryId")))
    select = Select(category_dropdown)
    # select.select_by_visible_text("890100   Club Withdrawals") # can select by visible text
    select.select_by_value("14180") # cleaner

    # select WISH account (2 selects) (always)
    accountselect_button = wait.until(EC.element_to_be_clickable((By.ID, "accountSelectButton")))
    accountselect_button.click() # click select button
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gridTable"))) # wait for popup to load
    popup_select_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'account-picker')]")))
    popup_select_button.click() # click popup select


    # PAYEE INFORMATION SECTION (all text can just for loop this)
    payee_info = {
        "PayeeFirstName": 'Bernette',
        "PayeeLastName": 'Chan',
        "PayeeStreet": "123 Fake Street",
        "PayeeCity": "San Luis Obispo",
        "PayeeState": "CA",
        "PayeeZipCode": "93405"
    }   
    for field_id, value in payee_info.items():
        field = wait.until(EC.presence_of_element_located((By.ID, field_id)))
        field.send_keys(value)


    # ADDITIONAL INFORMATION SECTION
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "pageResponse.Responses[fta42974783].FreeText")))
    email_field.send_keys('name@calpoly.edu')

    phone_field = wait.until(EC.presence_of_element_located((By.NAME, "pageResponse.Responses[fta43119126].FreeText")))
    phone_field.send_keys('1234567890')

    # select payment method
    # paymentmethod_buttonpath = f"//div[@class='radio']/label[contains(text(), '{label_text}')]/input" (depend on input)
    paymentmethod_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='41857276']"))) # selects issue payment (need to change number if different)
    paymentmethod_button.click()

    # event details (n/a) (always)
    field_ids = [
    "answerTextBox-45244583-free",
    "answerTextBox-47893182-free",
    "answerTextBox-47893183-free"
    ]
    for field_id in field_ids:
        field = wait.until(EC.presence_of_element_located((By.ID, field_id)))
        field.send_keys('N/A')

    # no to off campus facility rental (always)
    nooffcampus_button = wait.until(EC.element_to_be_clickable((By.ID, "47432212")))
    nooffcampus_button.click()

    # payment method (depend on input)
    payment_method = "Direct Deposit"  # Change to "Hold Check" if needed
    if payment_method == "Direct Deposit":
        radio_id = "42243575"
    elif payment_method == "Hold Check":
        radio_id = "41857287"
    else:
        radio_id = "41857288"  # Default to "Send Purchase Order"
    radio_button = wait.until(EC.element_to_be_clickable((By.ID, radio_id)))
    radio_button.click()

    # no to payment to services (always)
    noservices_button = wait.until(EC.element_to_be_clickable((By.ID, "41857296")))
    noservices_button.click()

    # no to payment to scholarship (always)
    noscholarship_button = wait.until(EC.element_to_be_clickable((By.ID, "42699760")))
    noscholarship_button.click()

    # no to cal poly name on items (always)
    nologo_button = wait.until(EC.element_to_be_clickable((By.ID, "41857303")))
    nologo_button.click()

    # receipt 1 checkbox
    receipt_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "41858630")))
    receipt_checkbox.click()
    # manually add receipt costs (if multiple)

    # click upload button & manually choose receipts pdf?
    uploadreceipts_button = wait.until(EC.element_to_be_clickable((By.ID, "fileUploadQuestion-11145673")))
    uploadreceipts_button.click()

    # no alcohol checkbox (always)
    noalc_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "41853987")))
    noalc_checkbox.click()

    # none of above hospitality radio button (always)
    hospitality_button = wait.until(EC.element_to_be_clickable((By.ID, "47893159")))
    hospitality_button.click()
    

except Exception as e:
    print(f"Error filling out form: {e}")


input("Press Enter to close the browser...")
# driver.quit()  # don't quit immediately