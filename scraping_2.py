# Link for the webdriver download: https://googlechromelabs.github.io/chrome-for-testing/

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configure the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Optional: start in full-screen
prefs = {"download.default_directory": ""}
options.add_experimental_option("prefs", prefs)

# ------------------
# define this ONCE at top of script
download_folder = "/Users/work/Downloads"
# ------------------

# downloaded_year = PANEL
login_page = "https://almastart.unibo.it/primo-explore/dbfulldisplay?docid=39UBO_ALMAE_DS5194399330007041&context=L&vid=39UBO_VU&lang=it_IT&adaptor=Local%20Search%20Engine&tab=jsearch_slot&query=any,contains,orbis&offset=0&databases=any,orbis"
#list_page = "https://orbis-r1.bvdinfo.com/version-20250619-3-0/Orbis/1/Companies/List"

list_page = "https://orbis-r1.bvdinfo.com/version-20250619-3-0/Orbis/1/Companies/List/Display/f74c9f8a-c5ff-401a-a547-571e7e19c896"

driver = webdriver.Chrome(options=options)

# Step 1: Go to the ORBIS access portal
driver.get(login_page)

# Pause to login manually
input("Please log in manually, then press ENTER here to continue...")

# Now ORBIS is loaded with the session active
# Step 2: Navigate to saved research set
driver.get(list_page)
time.sleep(10)
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Generate ranges from 1 to 9,012,251 with width 5000
def generate_ranges(start, end, width):
    ranges = []
    current = start
    while current <= end:
        range_end = min(current + width - 1, end)
        ranges.append((current, range_end))
        current += width
    return ranges

ranges = generate_ranges(1, 9012251, 5000)

# Print the ranges for verification
print(f"Total ranges to process: {len(ranges)}")
print(f"First 5 ranges: {ranges[:5]}")
print(f"Last 5 ranges: {ranges[-5:]}")

wait = WebDriverWait(driver, 15)

for i, (start_val, end_val) in enumerate(ranges):
    custom_filename = f"ITA_PANEL_{start_val}_{end_val}"
    print(f"\n🔄 Starting export {i+1}/{len(ranges)} for range: {start_val} to {end_val}")
    time.sleep(15)

    # Step 2: Click Export button
    try:
        export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-format='ExcelDisplay2007' and @data-export='list']")))
        export_btn.click()
        print("✅ Step 2: Clicked Excel export button.")
    except Exception as e:
        print("❌ Step 2: Failed to click export button:", e)
    time.sleep(5)
    
    # Step 2a: Set export filename
    try:
        filename_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "component_FileName"))
        )
        filename_input.clear()  # remove default text
        # custom_filename = f"ITA_PANEL_{start_val}_{end_val}"
        filename_input.send_keys(custom_filename)
        print(f"✅ Step 2a: Set filename to {custom_filename}.")
    except Exception as e:
        print("❌ Step 2a: Failed to set export filename:", e)

    # Step 3: Click Excel options dropdown
    try:
        options_btn = driver.find_element(By.XPATH, "//img[@data-toggle-target='div.formatExpertOptions']")
        options_btn.click()
        print("✅ Step 3: Clicked Excel options dropdown.")
    except Exception as e:
        print("❌ Step 3: Failed to click dropdown:", e)
    time.sleep(5)

    # Step 4: Select "Keep one record per line"
    try:
        record_option = driver.find_element(By.XPATH, "//input[@type='radio' and @name='component.MultipleValues' and @value='OneCompanyPerLine']")
        record_option.click()
        print("✅ Step 4: Selected 'Mantieni un rapporto per riga'.")
    except Exception as e:
        print("❌ Step 4: Failed to select option:", e)
    time.sleep(5)

    # Step 5: Reopen Excel options dropdown
    try:
        options_btn = driver.find_element(By.XPATH, "//img[@data-toggle-target='div.formatExpertOptions']")
        options_btn.click()
        print("✅ Step 5: Reopened Excel options dropdown.")
    except Exception as e:
        print("❌ Step 5: Failed to reopen dropdown:", e)
    time.sleep(5)

    # Step 6: Select "Range of companies"
    try:
        select = Select(driver.find_element(By.ID, "component_RangeOptionSelectedId"))
        select.select_by_value("Range")
        print("✅ Step 6: Selected 'A range of companies'.")
    except Exception as e:
        print("❌ Step 6: Failed to select range:", e)
    time.sleep(5)

    # Step 7: Enter 'From' value
    try:
        from_input = driver.find_element(By.NAME, "component.From")
        from_input.clear()
        from_input.send_keys(str(start_val))
        print("✅ Step 7: Entered 'From' value.")
    except Exception as e:
        print("❌ Step 7: Failed to enter 'From':", e)
    time.sleep(5)

    # Step 8: Enter 'To' value
    try:
        to_input = driver.find_element(By.NAME, "component.To")
        to_input.clear()
        to_input.send_keys(str(end_val))
        print("✅ Step 8: Entered 'To' value.")
    except Exception as e:
        print("❌ Step 8: Failed to enter 'To':", e)
    time.sleep(5)

    # Step 9: Tick 'Also send email' checkbox
    try:
        checkbox = driver.find_element(By.NAME, "component.Send")
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        if not checkbox.is_selected():
            checkbox.click()
        print("✅ Step 9: Checked 'Also send email'.")
    except Exception as e:
        print("❌ Step 9: Failed to click checkbox:", e)
    time.sleep(5)

    from selenium.webdriver.common.keys import Keys

    # Step 10: Enter email and press ENTER
    try:
        email_input = driver.find_element(By.ID, "component_EmailAddresses")
        email_input.clear()
        email_input.send_keys("alessiochiodin@hotmail.com")
        email_input.send_keys(Keys.RETURN)  # Simulating Enter key press
        print("✅ Step 10: Entered email address and pressed Enter.")
    except Exception as e:
        print("❌ Step 10: Failed to enter email or press Enter:", e)

    # Step 11: Click Export
    try:
        export_button = driver.find_element(By.XPATH, "//a[text()='Export']")
        export_button.click()
        print("✅ Step 11: Clicked Export button.")
    except Exception as e:
        print("❌ Step 11: Failed to click Export:", e)
    time.sleep(5)

    import os

    # Step 12: Wait for file to exist in download folder
    # expected_filename = f"ITA_{downloaded_year}_{start_val}_{end_val}.xlsx"
    expected_filename = f"{custom_filename}.xlsx"
    full_file_path = os.path.join(download_folder, expected_filename)

    print(f"⏳ Step 12: Waiting for file {expected_filename} to appear in download folder...")

    max_wait = 200  # (e.g. 10 min)
    interval = 5
    elapsed = 0

    while not os.path.exists(full_file_path) and elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval

    if os.path.exists(full_file_path):
        print(f"✅ Step 12: File {expected_filename} detected. Proceeding to next batch.")
    else:
        print(f"❌ Step 12: File {expected_filename} NOT found after {max_wait} seconds.")

    # Step 13: Close popup with JS click
    try:
        close_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@class='close px16' and @alt='X']"))
        )
        driver.execute_script("arguments[0].click();", close_btn)
        print("✅ Step 13: Closed export confirmation popup.")
    except Exception as e:
        print("❌ Step 13: Failed to close popup:", e)

    time.sleep(5)
    
    # Reload every 3 downloads to reset session
    if (i + 1) % 3 == 0:
        print("🔁 Reloading the saved search to reset session...")
        driver.get(list_page)
        time.sleep(30)

    # Optional: Add a longer break every 50 downloads to avoid overwhelming the system
    if (i + 1) % 50 == 0:
        print(f"🛑 Completed {i + 1} downloads. Taking a 5-minute break...")
        time.sleep(300)  # 5 minute break

print(f"\n🎉 All {len(ranges)} exports completed!")
driver.quit()