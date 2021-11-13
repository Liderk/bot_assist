"""
В этом модуле находятся классы для просмотров продавцов x-box
"""
from time import sleep

from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium_side.selenium_main import StartWebDriverBase


class CheckMvideo(StartWebDriverBase):
    """Проверка сайта Мвидео на наличие консоли """
    MAIN_URL = 'https://www.mvideo.ru/'

    def __init__(self):
        self.url = self.MAIN_URL
        super().__init__(self.url)

    def get_xbox_status(self):
        """
        Вбивает в поиск название консоли и смотрит ее статус
        :return:
        """

        search_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, '1')))

        self.send_text_like_human(search_field, 'Xbox Series X')
        search_field.send_keys(Keys.ENTER)

        x_box_link = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//a[contains(@title, ' Microsoft "
                                        "Xbox Series X')]")))
        sleep(2)
        x_box_link.click()

    def set_locations(self, location: str):
        """
        установка города поиска
        :param location: город для поиска
        :return:
        """
        try:
            close_banner = self.driver.find_element(By.TAG_NAME, 'button').click()
            location_el = self.driver.find_element(By.XPATH, "//div[@class='location ng-tns-c251-2']")
            location_el.click()
            input_location = self.driver.find_element(value='8')
            self.send_text_like_human(input_location, location)
            input_location.send_keys(Keys.ENTER)
            sleep(5)
            self.driver.send_keys(Keys.ENTER)
        except Exception as exp:
            logger.exception(f'Ошибка: {exp}')


class Check1C(StartWebDriverBase):
    """Проверка сайта 1с-интерес на наличие консоли """
    MAIN_URL = 'https://www.1c-interes.ru'

    def __init__(self):
        self.url = self.MAIN_URL
        super().__init__(self.url)

    def set_locations(self, location: str) -> None:
        """
        установка города поиска
        :param location: город для поиска
        :return:
        """

        location_tag = self.driver.find_element(By.XPATH, "//div/section/section//a/span[@class='city_name']")
        location_tag.click()
        input_location_field = self.driver.find_element(By.ID, 'city_choose')
        self.send_text_like_human(input_location_field, location)
        input_location_field.send_keys(Keys.ENTER)
        btn = self.driver.find_element(By.XPATH, '//fieldset/input[@class="btn-orange"]')
        print(btn.is_enabled())

        btn.click()

    def get_xbox_status(self):
        """
        Проверка статуса xbox
        """

        catalog = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Каталог товаров')
        catalog.click()
        games_and_consoles = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Игры и консоли')
        ActionChains(self.driver).move_to_element(games_and_consoles).perform()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Xbox Series X / S').click()
        status = self.driver.find_element(By.XPATH, '//h1[@class="H1_DESKTOP small-screen-hide"]')
        logger.info(status.text)


class CheckDNS(StartWebDriverBase):
    """Проверка сайта DNS на наличие консоли """
    MAIN_URL = 'https://www.dns-shop.ru/'

    def __init__(self):
        self.url = self.MAIN_URL
        super().__init__(self.url)


    def set_location(self):

mvideo = Check1C()
sleep(10)
mvideo.set_locations('Томск')
sleep(1)
mvideo.get_xbox_status()

sleep(3)
