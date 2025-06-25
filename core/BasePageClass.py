import os
from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import logging


class BasePage():
    title = None

    def __init__(self, driver):
        self.driver = driver
        # 等待页面标题出现
        try:
            WebDriverWait(self.driver, 5).until(
                expected_conditions.title_contains(self.title)
            )
        except:
            print("你的操作可能不在当前页面中，可能会引发异常{}".format(self.title))

    # 查找元素
    def find_element(self, locator):
        try:
            el = self.driver.find_element(*locator)
            logging.info(f'找到元素: {locator}')
            return el
        except:
            # 如果找不到元素，截图
            self.screen_shot(name=f'{locator}')
            logging.error("元素找不到：{}".format(locator))

    # 元素找不到时截图
    def screen_shot(self, name):
        path = f"./screen_shots/{name}"
        os.makedirs(path, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = os.path.join(path, ts + ".png")
        self.driver.save_screenshot(filename)

    # 等待元素可见
    def wait_element_visible(self, locator, timeout=2, poll=0.5):
        try:
            el = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(
                expected_conditions.visibility_of_element_located(locator)
            )
            logging.info(f'找到元素: {locator}')

            return el
        except:
            self.screen_shot(name=f'{locator}')
            logging.error("元素找不到{}".format(locator))

    # 等待元素可被点击
    def wait_element_clickable(self, locator, timeout=5, poll=0.5):
        try:
            el = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(
                expected_conditions.element_to_be_clickable(locator)
            )
            logging.info(f'找到元素: {locator}')

            return el
        except:
            self.screen_shot(name=f'{locator}')
            logging.error("元素找不到{}".format(locator))

    # 等待元素被加载
    def wait_element_presence(self, locator, timeout=2, poll=0.5):
        try:
            el = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(
                expected_conditions.presence_of_element_located(locator)
            )
            logging.info(f'找到元素: {locator}')

            return el
        except:
            self.screen_shot(name=f'{locator}')
            logging.error("元素找不到{}".format(locator))

    # 等待元素,等不到跳过
    def wait_element_visible_pass(self, locator, timeout=2, poll=0.5):
        try:
            el = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(
                expected_conditions.visibility_of_element_located(locator)
            )
            logging.info(f'找到元素: {locator}')

            return el
        except:
            pass

    # 点击元素
    def click(self, locator):
        # 当元素可被点击时再点击
        self.wait_element_clickable(locator).click()
        return self

    # 输入字符
    def write(self, locator, value=''):
        # 当元素被加载出来时再输入字符
        self.wait_element_presence(locator).send_keys(value)
        return self

    # 窗口滚动
    def scroll(self, height=None, width=None):
        if not height:
            height = 0
        if not width:
            width = 0
        js_code = "window.scrollTo({}, {});".format(width, height)
        self.driver.execute_script(js_code)
        return self

    # 移动到某个元素上面
    def move_to(self, locator):
        el = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(el).perform()
        return self

    # iframe切换
    def switch_frame(self, locator, timeout=2):
        WebDriverWait(self.driver, timeout=timeout).until(
            expected_conditions.frame_to_be_available_and_switch_to_it(locator)
        )
        return self
