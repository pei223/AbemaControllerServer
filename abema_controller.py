from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
import time
from config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import threading
from enum import Enum


class AppState(Enum):
    SWITCH_OFF = 1
    SWITCH_ON = 2
    FULL_SCREEN = 3

    @staticmethod
    def toggle_full_screen(state):
        if state == AppState.SWITCH_ON:
            return AppState.FULL_SCREEN
        return AppState.SWITCH_ON


class AbemaController:
    _instance = None

    def __init__(self):
        self._state = AppState.SWITCH_OFF
        self.driver = None

    def switch(self):
        if self._state == AppState.SWITCH_ON or self.driver:
            self._switch_off()
            return
        self._switch_on()

    def _switch_on(self):
        self._state = AppState.SWITCH_ON
        self.driver = webdriver.Chrome(Config.instance().driver_path)
        self.driver.get(Config.instance().abema_channel_url())
        self.driver.maximize_window()
        time.sleep(6)
        self.driver.refresh()
        self.driver.find_element_by_tag_name("body").click()

    def _switch_off(self):
        self._state = AppState.SWITCH_OFF
        self.driver.close()
        self.driver.quit()
        self.driver = None

    def channel_prev(self):
        try:
            # if self._state == AppState.FULL_SCREEN:
            #     self.toggle_full_screen()
            actions = ActionChains(self.driver)
            actions.move_to_element(self.driver.find_element_by_class_name("com-tv-TVScreen__player")).perform()
            self.driver.find_elements_by_class_name("abm_1a881647_a")[0].click()
        except ElementNotInteractableException as e:
            print(e.msg)

    def channel_next(self):
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(self.driver.find_element_by_class_name("com-tv-TVScreen__player")).perform()
            self.driver.find_elements_by_class_name("abm_1a881647_a")[2].click()
        except ElementNotInteractableException as e:
            print(e.msg)

    def toggle_full_screen(self):
        def func(driver):
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element_by_class_name("com-tv-TVScreen__player")).perform()
            wait = WebDriverWait(driver, 120)  # 最大10秒
            elem = wait.until(
                expected_conditions.element_to_be_clickable((By.CLASS_NAME, "com-tv-TVController__fullscreen")))
            elem.click()

        threading.Thread(target=func, args=(self.driver,)).start()
        self._state = AppState.toggle_full_screen(self._state)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AbemaController()
        return cls._instance
