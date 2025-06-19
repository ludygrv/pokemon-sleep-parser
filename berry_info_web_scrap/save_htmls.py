from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup
opts = Options()
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)

driver.get("https://pks.raenonx.cc/en/berry/1")

# Wait up to 15s for the hydrated JSON blob to include the word "calculations"
WebDriverWait(driver, 15).until(
    EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, "script#__NEXT_DATA__"),
        "calculations"
    )
)

# Now grab the full JSON payload
next_data = driver.find_element(By.CSS_SELECTOR, "script#__NEXT_DATA__").get_attribute("textContent")
driver.quit()

import json
data = json.loads(next_data)
levels = data["props"]["pageProps"]["berry"]["calculations"]["levels"]
print("First 5 entries:", levels[:5])
