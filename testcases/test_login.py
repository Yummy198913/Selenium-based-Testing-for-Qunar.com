import pytest
from selenium import webdriver
from core.pom import *
from data.data import *
import logging


@pytest.mark.parametrize(
    "username, password, code",
    read_excel('login_data.xlsx')
)
def test_login(driver, username, password, code):
    '''
    测试用例，模拟登录操作
    :param driver:
    :return:
    '''
    driver.get(LoginPage.url)
    page = LoginPage(driver)
    page_code = page.login(username, password)

    logging.info(f'page_code: {page_code}'.center(50, '-'))
    logging.info(f'code: {code}'.center(50, '-'))

    assert page_code == code

