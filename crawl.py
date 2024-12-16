from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import csv
import os
from selenium.webdriver.chrome.options import Options

# Selenium Driver Setup
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome()

# Constants
URL = "https://vietschool.vn/home/tracuudiemtracnghiem"
FIRST_SBD = 660001  # Starting ID
LAST_SBD = 660139   # Ending ID
CSV_FILE = "k12.csv"
FIRST_RUN = False
# Function Definitions
def setup_csv():
    global FIRST_RUN
    """Deletes old CSV file and creates a new one with the header."""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["SBD", "Họ và tên", "Ngày sinh", "Mã đề", "Tên đợt chấm", "Điểm số"])
    csvfile.close()

def start():
    """Initializes the selection process for province, district, and school."""
    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKTinh1-container"))
    )
    checklist.click()

    # Select province
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("HAI P")
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.05)

    # Select district
    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKHuyenID1-container"))
    )
    checklist.click()
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("TR")
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.2)

    # Select school
    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKTruongID1-container"))
    )
    checklist.click()
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("FPT")
    input_element.send_keys(Keys.ENTER)

    # Enter first student ID
    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.send_keys(str(FIRST_SBD))

    # Click search button
    button = driver.find_element(By.ID, "btnFinds")
    button.click()

def get_mark_and_write():
    """Fetches marks and writes them to a CSV file."""
    time.sleep(0.2)

    try:
        # Wait for the elements to load
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='fgKetQua']//div[contains(@class, 'wj-row')]"))
        )

        # Initialize an empty list for processed data
        table_data = []

        # Process rows, optionally skipping the first
        for i, row in enumerate(rows): # The continue keyword is used to end the current iteration in a for loop (or a while loop), and continues to the next iteration.
            if i == 9:
                continue
            # Extract text content from each cell
            cells = row.find_elements(By.XPATH, ".//div[contains(@class, 'wj-cell')]")
            cell_data = [cell.text.strip() for cell in cells]
            cell_data = cell_data[1:]  # Remove the first item (STT column)

            # Append non-empty rows to the table data
            if any(cell_data):
                table_data.append(cell_data)

        # Write data to CSV file
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in table_data:
                csv_writer.writerow(row)

        print("Write done.")
    except Exception as e:
        print(f"An error occurred: {e}")


def doi_sbd(new_sbd):
    """Updates the student ID and fetches the corresponding marks."""
    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.clear()
    input_element.send_keys(str(new_sbd))
    print(new_sbd)

    button = driver.find_element(By.ID, "btnFinds")
    button.click()
    get_mark_and_write()

# Main Execution
if __name__ == "__main__":
    # Setup CSV file
    setup_csv()

    # Navigate to URL
    driver.get(URL)
    time.sleep(5)

    # Initial setup
    start()
    time.sleep(0.1)

    # Process student IDs
    for sbd in range(FIRST_SBD, LAST_SBD + 1):
        doi_sbd(sbd)

    # Close the driver
    input("Press Enter to exit...")
    driver.quit()
