from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

listInputForm = [];

def setup():
    print('⚙️ Setting up')
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')  # Menjalankan Chrome di background
    # option.add_argument('--no-sandbox')  # Menghindari masalah di server
    # option.add_argument('--disable-dev-shm-usage')
    option.add_experimental_option('detach', True)
    driver = webdriver.Edge()
    driver.get('https://forms.gle/RCqqhbFLyFPt17hX8')
    return driver

def teardown(driver):
    print('\n🗑️ Tearing down')
    time.sleep(2)
    driver.quit()

def formatListInput(label, type, options):
    return { 'label': label, 'type': type, 'options': options };

def identifyForm():
    global listInputForm
    driver = setup()
    print('🔍 Identifying Form...')
    time.sleep(6)
    listContainerInput = driver.find_elements(by=By.CLASS_NAME, value='Qr7Oae')
    if len(listContainerInput) == 0:
        print('🤌 Nothing to found')
    else:
        print(f'🤟 Found {len(listContainerInput)} container input')
        for idx, containerInput in enumerate(listContainerInput):
            print(f'\n🫸 Checking container input {idx + 1}')
            time.sleep(2)
            listInputForm.append(checkInputType(containerInput))
    listInputForm = json.dumps(listInputForm)
    teardown(driver)
    print('Identifying completed')
    print('=====================\n')

def checkInputType(containerInput):
    # ? Check input is text
    try:
        textInputLabel = containerInput.find_element(by=By.XPATH, value='.//*[@role="heading"]').text
        containerInput.find_element(by=By.XPATH, value='.//input[@class="whsOnd zHQkBf"]')
        print('Input type is text')
        print('Label: ' + textInputLabel.replace('\n', ' ').strip())
        return formatListInput(label=textInputLabel, type='text', options=[])
    except Exception as e:
        pass

    # ? Check input is radio
    try:
        radioInputLabel = containerInput.find_element(by=By.XPATH, value='.//*[@role="heading"]').text
        radioInput = containerInput.find_elements(by=By.XPATH, value='.//*[contains(@class, "Od2TWd") and not(contains(@aria-disabled, "true"))]')
        if (len(radioInput) != 0):
            print('Input type is radio')
            print('Label: ' + radioInputLabel.replace('\n', ' ').strip())
            print('Options:')
            radioValue = []
            for idx, radio in enumerate(radioInput):
                # ? Kisi pilgan
                hasFieldIndex = radio.get_attribute('data-field-index')
                if hasFieldIndex is not None:
                    print('Ini kisi pilgan')
                    return formatListInput(label='-', type='-', options=[])
                else:
                    radioValue.append(radio.get_attribute('data-value'))
                print(f'{idx}, {radioValue}')
            return formatListInput(label=radioInputLabel, type='radio', options=radioValue)
    except Exception as e:
        pass

    # ? Check input is dropdown
    try:
        dropdownInputLabel = containerInput.find_element(by=By.XPATH, value='.//*[@role="heading"]').text
        containerInput.find_element(by=By.XPATH, value='.//*[contains(@role, "listbox")]').click()
        listDropdownInput = containerInput.find_elements(by=By.XPATH, value='.//*[contains(@class, "MocG8c")]')
        print('Input type is dropdown')
        print('Label: ' + dropdownInputLabel.replace('\n', ' ').strip())
        print('Options:')
        dropdownValue = []
        for idx, dropdownInput in enumerate(listDropdownInput):
            if idx > 0:
                dropdownValue.append(dropdownInput.get_attribute('data-value'))
                print(f'{idx}, {dropdownValue}')
        return formatListInput(label=dropdownInputLabel, type='dropdown', options=dropdownValue)
    except Exception as e:
        pass

    # ? Check input is checkbox
    try:
        checkboxInputLabel = containerInput.find_element(by=By.XPATH, value='.//*[@role="heading"]').text
        listCheckboxInput = containerInput.find_elements(by=By.XPATH, value='.//*[contains(@class, "uVccjd")]')
        if len(listCheckboxInput) > 0:
            print('Input type is checkbox')
            print('Label: ' + checkboxInputLabel.replace('\n', ' ').strip())
            checkboxValue = []
            for checkboxInput in listCheckboxInput:
                checkboxValue.append(checkboxInput.get_attribute('data-answer-value'))
                print(checkboxValue)
            return formatListInput(label=checkboxInputLabel, type='checkbox', options=checkboxValue)
    except Exception as e:
        pass

def fillForm():
    print(listInputForm)
    # for inputForm in json.loads(listInputForm):
    #     print(inputForm)

if __name__ == '__main__':
    print('🚀 Running App')
    identifyForm()
    fillForm()