import random
from time import sleep

from loguru import logger
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class StartWebDriverBase:
    """
    Базовый класс для работы с сайтами
    запускает веб драйвер
    """

    def __init__(self, url_link: str, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument('-headless')
        self.url = url_link
        self.driver = Firefox(options=self.options)
        self.driver.implicitly_wait(20)
        self.driver = self.get_url(url_link)

    def __del__(self):
        """
        Определим деструктор класса как StartWebDriverBase удаление и
        закрытие текущих соединений
        :return: None
        """
        try:
            self.driver_quit()
        except Exception as exp:
            logger.exception(f'Ошибка - {exp}')
            raise

    def get_url(self, url_link: str = None):
        """
        Проходит по ссылке
        :return: driver obj
        """
        max_attempt = 14
        logger.info(f'Идем на страницу - {url_link:}')
        while max_attempt:
            try:
                if url_link:
                    self.url = url_link
                self.driver.get(url_link)
                logger.info('Удачная загрузка страницы')
                return self.driver
            except Exception as exp:
                logger.exception(f'Ошибка - {exp}')
                max_attempt -= 1
        raise Exception(f'Глобальная ошибка, не удалось войти на "{url_link}"')

    @staticmethod
    def send_text_like_human(element, text_value: str) -> None:
        """
         Вводит текст по буквам с непостоянными паузами.
         Простая эмуляция человека
        :param element: найденный элемент/поле для ввода текста
        :param text_value: текст для ввода
        :return: None
        """
        for symbol in text_value:
            element.send_keys(symbol)
            sleep(random.uniform(0.1, 0.4))

    def driver_close(self):
        """
        метод закрытия текущего соединения
        :return: None
        """
        try:
            self.driver.close()
            logger.info('Закрыли текущее подключение')

        except Exception as exp:
            logger.exception(f'Ошибка - {exp}')
            raise

    def driver_quit(self):
        """
        в метод выхода из драйвера из драйвера
        :return: None
        """
        try:
            self.driver_close()
            self.driver.quit()
            logger.info('Вышли из браузера')

        except Exception as exp:
            logger.exception(f'Ошибка - {exp}')
            raise
