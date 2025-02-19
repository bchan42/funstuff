# # automating part
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pickle # save and load cookies
# import time


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
#                           options=webdriver.ChromeOptions())
# # driver = webdriver.Chrome('/Users/bernettechan/chromedriver-mac-x64/chromedriver') # initialize chromedriver

# # go to home page
# driver.get('https://now.calpoly.edu/') 
# time.sleep(3)

# # wait for "SIGN IN" link to be clickable and then click
# try:
#     signin_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.LINK_TEXT, "SIGN IN"))
#     )
#     signin_button.click()  # click on Sign In button
# except Exception as e:
#     print(f"Error clicking sign in: {e}")

# time.sleep(3)

# # manula log in
# print("Please log in manually")
# time.sleep(10) # long enough to login

# cookies = driver.get_cookies()
# with open("cookies.pkl", "wb") as cookie_file:
#     pickle.dump(cookies, cookie_file) # save cookies after manual login

# # open site again with cookies loaded
# driver.get('https://now.calpoly.edu/') # open site again, this time logged in
# time.sleep(1)

# # load cookies from file & add to browser
# with open("cookies.pkl", "rb") as cookie_file:
#     cookies = pickle.load(cookie_file)
#     for cookie in cookies:
#         driver.add_cookie(cookie) # add each cookie to browser

# driver.refresh() # make sure session applied correctly

# driver.get("https://now.calpoly.edu/actionCenter/organization/wish/Finance/CreatePurchaseRequest") # PRF page
# time.sleep(5)



# # driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import os

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # initialize chromedriver

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
    
    # Now access the form
    driver.get('https://now.calpoly.edu/actionCenter/organization/wish/Finance/CreatePurchaseRequest')  # PRF form page
    time.sleep(5)

# check if you're on the form page
print("Now on the PRF form!")

# Add debugging output to keep the browser open and debug what's happening
input("Press Enter to close the browser...")

# driver.quit()  # Don't quit immediately; let user inspect if necessary