from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleForm:
    def __init__(self):
        self.listInputForm = []
        self.currentJob = 1
        pass
    
    def __setup(self, url):
        print('⚙️ Setting up')
        option = webdriver.EdgeOptions()
        option.add_argument('--headless')
        # option.add_argument('--no-sandbox')
        # option.add_argument('--disable-gpu')
        # option.add_argument('--disable-dev-shm-usage')
        # option.add_experimental_option('detach', True)
        driver = webdriver.Edge(options=option)
        driver.get(url)
        return driver

    def __teardown(self, driver):
        print('\n🗑️ Tearing down')
        driver.quit()

    def __formatListInput(self, label, type, options):
        return { 'label': label, 'type': type, 'options': options };

    def __checkInputType(self, containerInput):
            # ? Check input is text
            try:
                textInputLabel = containerInput.find_element(by=By.XPATH, value='.//*[@role="heading"]').text
                containerInput.find_element(by=By.XPATH, value='.//input[@class="whsOnd zHQkBf"]')
                print('Input type is text')
                print('Label: ' + textInputLabel.replace('\n', ' ').strip())
                return self.__formatListInput(label=textInputLabel, type='text', options=[])
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
                            return self.__formatListInput(label='-', type='-', options=[])
                        else:
                            radioValue.append(radio.get_attribute('data-value'))
                        print(f'{idx}, {radioValue}')
                    return self.__formatListInput(label=radioInputLabel, type='radio', options=radioValue)
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
                return self.__formatListInput(label=dropdownInputLabel, type='dropdown', options=dropdownValue)
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
                    return self.__formatListInput(label=checkboxInputLabel, type='checkbox', options=checkboxValue)
            except Exception as e:
                pass

    def identify(self, url: str):
        self.currentJob = 1
        driver = self.__setup(url)
        self.listInputForm = []
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
                self.listInputForm.append(self.__checkInputType(containerInput))
        self.listInputForm = self.listInputForm
        self.__teardown(driver)
        print('Identifying completed')
        print('=====================\n')
        return self.listInputForm

    def filling(self, url: str, data: any):
        start_time = time.time()
        driver = self.__setup(url)
        self.currentJob = 1
        currentJob = self.currentJob
        self.currentJob += 1
        print(f'Finding form - ({currentJob})')
        containerInputForm = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Qr7Oae'))
        )
        print(f'Form founded, start fill ({currentJob})')
        for idx, inputForm in enumerate(data):
            time.sleep(0.5)
            inputAnswer = inputForm['answer']

            if inputForm['type'] == 'text':
                try:
                    WebDriverWait(containerInputForm[idx], 10).until(
                        EC.visibility_of_element_located((By.XPATH, './/*[@class="whsOnd zHQkBf"]'))
                    ).send_keys(f'{inputAnswer})')
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
        print(f'Submited form ({currentJob})')

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="c2gzEf"]/a'))
        ).click()
        print(f'Button next form clicked ({currentJob})')
        self.__teardown(driver)
        end_time = time.time()
        elapsed_time = end_time - start_time
        result = f'Form filled ({currentJob}): {elapsed_time:.2f} seconds'
        print(result)
        return result