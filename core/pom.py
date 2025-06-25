import random
import time
from selenium.webdriver.common.by import By
from core.BasePageClass import *
import logging


class LoginPage(BasePage):
    '''
    去哪儿网登录页面
    '''
    url = 'https://flight.qunar.com/'

    def __init__(self, driver):
        super().__init__(driver)

        self.login_button = (By.XPATH, '//a[text()="登录"]')  # 网站首页登录按钮

        self.passwd_login_button = (By.XPATH, '//div[text()="密码登录"]')  # 网站登录页 “密码登录” 按钮

        self.username_edit = (By.XPATH, '//input[@id="username"]')  # 用户名输入框

        self.passwd_edit = (By.XPATH, '//input[@id="password"]')  # 密码输入框

        self.policy_confirm_button = (By.XPATH, '//*[@id="agreement"]')  # 用户协议check box

        self.login_enter_button = (By.XPATH, '//span[text()="登录"]')  # 登录按钮

        # 滑动按钮
        self.slide_button = (By.XPATH,
                             '//*[@id="app"]/div/div[2]/div/div[1]/div[3]/div/div[5]/div/div/div[3]/div[3]/i')

        # 滑动背景
        self.slide_bg = (By.XPATH,
                         '//*[@id="app"]/div/div[2]/div/div[1]/div[3]/div/div[5]/div/div/div[3]/div[2]')

        # 输入用户名或者密码可能出现的几种情况对应的元素
        self.user_name_warning = (By.XPATH, '//span[text()="请输入手机/邮箱/用户名"]')
        self.passwd_warning = (By.XPATH, '//span[text()="请输入密码"]')
        self.username_format_warning = (By.XPATH, '//span[text()="用户名格式错误"]')
        self.passwd_format_warning = (By.XPATH, '//span[text()="密码格式错误"]')
        self.incorrect_warning = (By.XPATH, '//span[text()="用户名或密码错误"]')


    def login(self, username, password):
        # 点击登录
        logging.info('点击首页登录按钮'.center(10, '-'))
        self.click(self.login_button)

        logging.info('点击使用密码登录'.center(10, '-'))
        self.click(self.passwd_login_button)  #点击使用密码登录

        logging.info('输入用户名'.center(10, '-'))
        self.write(self.username_edit, username)

        logging.info('输入密码'.center(10, '-'))
        self.write(self.passwd_edit, password)

        logging.info('确认协议'.center(10, '-'))
        self.click(self.policy_confirm_button)

        logging.info('确认登录'.center(10, '-'))
        self.click(self.login_enter_button)

        # 如果有滑动验证码出现，就模拟滑动
        if self.wait_element_visible_pass(self.slide_button):
            logging.info('模拟滑动验证'.center(10, '-'))
            distance = self.find_element(self.slide_bg).size['width']
            tracks = self.get_slide_tracks(distance)
            # 执行滑动操作
            slide_button_el = self.find_element(self.slide_button)
            self.slide_verify(slide_button_el, tracks)

        msg = self.get_msg()

        return msg


    def get_msg(self):
        if self.wait_element_visible_pass(self.user_name_warning):
            return 401
        if self.wait_element_visible_pass(self.passwd_warning):
            return 402
        if self.wait_element_visible_pass(self.username_format_warning):
            return 404
        if self.wait_element_visible_pass(self.passwd_format_warning):
            return 405
        if self.wait_element_visible_pass(self.incorrect_warning):
            return 403

        current_url = self.driver.current_url
        if current_url == 'https://flight.qunar.com/':
            return 200
        else:
            return None

    def get_slide_tracks(self, distance):
        """
        生成滑动轨迹，模拟人类先加速后减速的行为
        """
        # 轨迹列表
        tracks = []
        # 当前位置
        current = 0
        # 减速阈值
        mid = distance * 1 / 4
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 60
            else:
                # 加速度为-3
                a = -3

            # 初速度v0
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t * 2
            # 当前位置
            current += move

            # 如果距离大于总距离，取总距离
            if current > distance:
                move = distance - (current - move)
                tracks.append(move)
                break

            tracks.append(move)

        # 添加一些小的回退，更像人类行为
        tracks.extend([-3, -2, -1])
        return tracks

    def slide_verify(self, slider, tracks):
        """
        执行滑动操作
        """
        action = ActionChains(self.driver)

        # 按住滑块
        action.click_and_hold(slider).perform()

        # 按照轨迹滑动
        for track in tracks:
            action.move_by_offset(track, 0).perform()
            # 添加随机延时，模拟人类思考时间
            time.sleep(random.uniform(0.01, 0.03))

        # 随机抖动
        action.move_by_offset(random.randint(-3, 3), random.randint(-3, 3)).perform()

        # 保持一段时间
        time.sleep(random.uniform(0.5, 1.0))

        # 释放滑块
        action.release().perform()

        # 等待验证结果
        time.sleep(1)