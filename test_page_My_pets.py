import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('c:/chromedriver.exe')
    # Переходим на страницу авторизации а потом на страницу мои питомцы
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.find_element(By.ID, 'email').send_keys('algan3@yandex.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('123456')

    wait = WebDriverWait(pytest.driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, u"Мои питомцы"))).click()

    yield
    pytest.driver.close()


# тест1 Присутствуют все питомцы.
def test_show_all_my_pets():
    pytest.driver.implicitly_wait(10)

    tablet = pytest.driver.find_element(By.XPATH, '(html/body/div[1]/div[1]/div[1])').text
    my_pets_count  = int(''.join(map(str, re.findall(r'\d+', tablet)[0])))
    all_str = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr)')
    assert len(all_str) == my_pets_count

    print("На странице все питомцы")



# тест2 Хотя бы у половины питомцев есть фото.
def test_show_my_pets_foto():
    images = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/th/img)')
    count = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != "":
            count += 1
        else:
            count += 0
    print("всего питомцев:", len(images))
    print("фото есть у:", count)
    assert len(images) <= count * 2
    print("питомцев с фото не меньше половины всех питомцев")


# тест3  у всех питомцев есть имя порода возраст
def test_show_my_pets():
    print(" тест У всех питомцев есть имя, возраст и порода")
    name = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    for i in range(len(name)):
        assert name[i].text != ''
    print("имя есть у всех питомцев")
    animal_type = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[2])')
    for i in range(len(animal_type)):
        assert animal_type[i].text != ''
    print("порода есть у всех питомцев")
    age = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[3])')
    for i in range(len(age)):
        assert age[i].text != ''
    print("возраст есть у всех питомцев")


# тест4 у всех питомцев разные имена
def test_all_my_pets_differernt_name():
    names = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    list_names = []
    for x in names:
        name = x.text
        list_names.append(name)
    lst_2 = list(set(list_names))
    assert len(list_names) == len(lst_2)


# тест5 В списке нет повторяющихся питомцев. (Сложное задание).
def test_all_my_pets_differernt_pets():
    wait = WebDriverWait(pytest.driver, 10)
    names = wait.until(EC.visibility_of_any_elements_located((By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr)')))
    list_names = []
    for x in names:
        name = x.text
        list_names.append(name)
    lst_2 = list(set(list_names))
    assert len(list_names) == len(lst_2)
    print("в списке нет повторяющихся записей питомцев")