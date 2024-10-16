from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

listInputForm = [
  {
    "label": "Pertanyaan dropdown\n*",
    "options": [
      "Tak suka",
      "Biasa",
      "Suka"
    ],
    "type": "dropdown",
    "answer": "Biasa"
  },
  {
    "label": "Pertanyaan teks singkat\n*",
    "options": [],
    "type": "text",
    "answer": "asd"
  },
  {
    "label": "Pertanyaan pilgan\n*",
    "options": [
      "Ini jawaban 1",
      "Ini jawaban 2"
    ],
    "type": "radio",
    "answer": "Ini jawaban 1"
  },
  {
    "label": "Pertanyaan kotak centang\n*",
    "options": [
      "Centang satu",
      "Centang dua"
    ],
    "type": "checkbox",
    "answer": "Centang dua"
  },
  {
    "label": "Pertanyaan linear\n*",
    "options": [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10"
    ],
    "type": "radio",
    "answer": "2"
  }
]

def setup():
    options = webdriver.EdgeOptions()
    # options.add_argument('--headless')  # Menjalankan Chrome di background
    # options.add_argument('--no-sandbox')  # Menghindari masalah di server
    # options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('detach', True)
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Edge(options=options)

    driver.get('https://forms.gle/X2T5GFj991btdcWy7')
    return driver

def teardown(driver):
    print('\n🗑️ Tearing down')
    time.sleep(2)
    driver.quit()

def filling():
    driver = setup()
    for count in range(2):
        print(count)
        containerInputForm = driver.find_elements(by=By.CLASS_NAME, value='Qr7Oae')
        containerInputForm = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Qr7Oae'))
        )
        for idx, inputForm in enumerate(listInputForm):
            time.sleep(0.5)
            inputAnswer = inputForm['answer']

            if inputForm['type'] == 'text':
                try:
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.visibility_of_element_located((By.XPATH, './/*[@class="whsOnd zHQkBf"]'))
                    ).send_keys(f'{inputAnswer} ({count})')
                except Exception as e:
                    pass

            if inputForm['type'] == 'radio':
                try:
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.element_to_be_clickable((By.XPATH, f'.//*[contains(@class, "Od2TWd") and not(contains(@aria-disabled, "true")) and @data-value="{inputAnswer}"]'))
                    ).click()
                except Exception as e:
                    pass

            if inputForm['type'] == 'dropdown':
                try:
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.element_to_be_clickable((By.XPATH, './/*[contains(@role, "listbox")]'))
                    ).click()
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.element_to_be_clickable((By.XPATH, f'.//div[@role="option" and @data-value="{inputAnswer}"]/span'))
                    ).click()
                except Exception as e:
                    pass

            if inputForm['type'] == 'checkbox':
                try:
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.element_to_be_clickable((By.XPATH, f'.//*[contains(@class, "uVccjd") and @data-answer-value="{inputAnswer}"]'))
                    ).click()
                except Exception as e:
                    pass

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Submit"]/span/span'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="c2gzEf"]/a'))
        ).click()
        count += 1;
    teardown(driver)

if __name__ == '__main__':
    print('🚀 Start app\n')
    filling()