from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.chrome.options import Options

def get_the_last(cnt):
    index = 0
    for i in range(0,len(cnt)):
        if cnt[i] == ">":
            index = i
    return index

def chia_mang(mang, so_mang_con):
  """Chia một mảng thành nhiều mảng con bằng nhau.

  Args:
    mang: Mảng cần chia.
    so_mang_con: Số lượng mảng con muốn tạo.

  Returns:
    Một danh sách chứa các mảng con.
  """

  do_dai_mang_con = len(mang) // so_mang_con
  mang_con = []
  for i in range(0, len(mang), do_dai_mang_con):
    mang_con.append(mang[i:i + do_dai_mang_con])
  return mang_con

def start():

    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKTinh1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("HAI P")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.05)

    # ---------------------------
    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKHuyenID1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("TR")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.2)
    # ---------------------------
    checklist = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-cboDKTruongID1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("FPT")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)

    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.send_keys(str(firstsbd))

    button = driver.find_element(By.ID, "btnFinds")
    button.click()
    get_mark_and_write()

def get_mark_and_write():
    time.sleep(0.1)
    header_written = False  # To track if the header has been written

    try:
        # Wait for the elements to load
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='fgKetQua']//div[contains(@class, 'wj-row')]"))
        )

        # Initialize an empty list for processed data
        table_data = []

        for row in rows:
            # Find all cell elements within a row
            cells = row.find_elements(By.XPATH, ".//div[contains(@class, 'wj-cell')]")
            # Extract text content from each cell
            cell_data = [cell.text.strip() for cell in cells]
            # Exclude the first column (STT)
            cell_data = cell_data[1:]  # Remove the first item (STT column)
            # Append non-empty rows to the table data
            if any(cell_data):  # Skip empty rows
                table_data.append(cell_data)

        # Define the header
        header = ["SBD", "Họ và tên", "Ngày sinh", "Mã đề", "Tên đợt chấm", "Điểm số"]

        # Open the file in append mode
        with open("k12.csv", "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)

            # Check if the file is empty (write header only once)
            if not header_written:
                with open("k12.csv", "r", encoding="utf-8") as readfile:
                    if not readfile.read().strip():  # File is empty
                        csv_writer.writerow(header)
                        header_written = True

            # Write the cleaned data
            for row in table_data:
                csv_writer.writerow(row)

        print("Write done.")
    except Exception as e:
        print(f"An error occurred: {e}")


def doi_sbd(new_sbd):
    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.clear()
    input_element.send_keys(str(new_sbd))
    print(new_sbd)

    button = driver.find_element(By.ID, "btnFinds")
    button.click()
    get_mark_and_write()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome()

# Navigate to url
driver.get("https://vietschool.vn/home/tracuudiemtracnghiem")
time.sleep(10)

firstsbd=122001
FirstTimeRun = True
start()
FirstTimeRun = False
time.sleep(0.1)
for sbd in range(firstsbd+1,firstsbd+308):
    doi_sbd(sbd)

input()
driver.quit()