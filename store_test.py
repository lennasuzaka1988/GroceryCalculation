from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Initializing the webdriver
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-popup-blocking')
options.add_argument('--enable-javascript')
options.add_argument('--disable-notifications')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)


def store_navigation():
    driver.get('https://www.sprouts.com')

    # Waiting for that damn initial popup
    click_maybe_later_text = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="pop-up-dismiss"]')),
    )
    click_maybe_later_text.click()


def kansas_city_store_722():
    # Swap to Kansas City store via Store's Specials buttons
    time.sleep(5)
    specials = WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="specials-banner-desktop"]')))
    specials.click()
    time.sleep(5)
    frames = driver.find_element(By.TAG_NAME, 'iframe:nth-child(2)')
    print(frames)
    # print(driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe:nth-child(1)')))

    # zip_text = driver.find_element(By.CSS_SELECTOR, '#postal-input')
    # zip_text.send_keys('64154' + Keys.ENTER)
    # driver.switch_to.default_content()


store_navigation()


kansas_city_store_722()

# public class SwitchToFrame_ID {
# public static void main(String[] args) {
#
# 		WebDriver driver = new FirefoxDriver(); //navigates to the Browser
# 	    driver.get("http://demo.guru99.com/test/guru99home/");
# 	       // navigates to the page consisting an iframe
#
# 	       driver.manage().window().maximize();
# 	       driver.switchTo().frame("a077aa5e"); //switching the frame by ID
#
# 			System.out.println("********We are switch to the iframe*******");
#      		driver.findElement(By.xpath("html/body/a/img")).click();
#   		    //Clicks the iframe
#
#   			System.out.println("*********We are done***************");
#       }
# }