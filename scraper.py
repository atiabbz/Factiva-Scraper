from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from getpass import getpass
import time
import os

USER_ID = input("HKU Portal UID / Library card number: ")
PASSWORD = getpass("PIN: ")
FORBIDDEN_CHARS = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)

FACTIVA_URL = "https://julac-hku.alma.exlibrisgroup.com/view/action/uresolver.do?operation=resolveService&package_service_id=15754959500003414&institutionId=3414&customerId=3405"

driver.get(FACTIVA_URL)

userIdField = driver.find_element_by_css_selector('input[name="userid"]')
userIdField.send_keys(USER_ID)

passwordField = driver.find_element_by_css_selector('input[name="password"]')
passwordField.send_keys(PASSWORD)

submitButton = driver.find_element_by_css_selector('input[name="submit"]')
submitButton.click()

dateSelector = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "dr"))
)
dateSelector.click()

allDatesOption = driver.find_element_by_css_selector('option[value="_Unspecified"]')
allDatesOption.click()
dateSelector.click()

regionPicker = driver.find_element_by_css_selector("#reTab > .pnlTabArrow")
regionPicker.click()
regionField = driver.find_element_by_id("reTxt")
regionField.send_keys("Hong Kong")
regionFieldSubmitButton = driver.find_element_by_id("reLkp")
regionFieldSubmitButton.click()
hongKongOption = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[code="re_hkong"]'))
)
hongKongOption.click()

englishOption = driver.find_element_by_css_selector('span[companyid="la_en"]')
englishOption.click()
languagePicker = driver.find_element_by_css_selector("#laTab > .pnlTabArrow")
languagePicker.click()
tradChineseOption = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[code="la_zhtw"]'))
)
tradChineseOption.click()

searchSubmitButton = driver.find_element_by_id("btnSearchBottom")
searchSubmitButton.click()

# headlinesTable = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'headlines')))
# allHeadlines = driver.find_elements_by_class_name('zhtwHeadline')
# returnLink = driver.find_element_by_id('returnToHeadlines')

WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "sources")))

allSources = driver.find_elements_by_css_selector("#sources .discovery-items .cItem")

allSources[0].click()

# subjects change for each source

WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.ID, "newsSubjects"))
)


overlayBackground = driver.find_element_by_id("__overlayBackground")
while "display: none" not in overlayBackground.get_attribute("style"):
    pass

allSubjects = driver.find_elements_by_css_selector(
    "#newsSubjects .discovery-items .cItem"
)
allSubjects[0].find_element_by_class_name("ellipsis").click()
while "display: none" not in driver.find_element_by_id(
    "__overlayBackground"
).get_attribute("style"):
    pass

headlinesTable = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.ID, "headlines"))
)
allHeadlines = driver.find_elements_by_class_name("zhtwHeadline")

for headline in allHeadlines:
    filename = headline.text
    for char in FORBIDDEN_CHARS:
        if char in filename:
            filename = filename.replace(char, "_")
    with open(f"{filename}.txt", "w", encoding="utf-8") as articleFile:
        headline.click()
        articleBody = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[class="article zhtwArticle"]')
            )
        )
        articleFile.write(articleBody.text)
        newFilename = articleBody.text[articleBody.text.rfind("Document ") :].strip()
        time.sleep(1)
        returnLink = driver.find_element_by_id("returnToHeadlines")
        returnLink.click()
    os.rename(f"{filename}.txt", f"{newFilename}.txt")
