"""
В этом модуле находятся классы для просмотров продавцов x-box
"""
from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa
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
        location_tag = self.driver.find_element(By.CSS_SELECTOR, 'a.opener span.city_name')
        location_tag.click()


mvideo = Check1C()
mvideo.set_locations('Томск')

sleep(3)
