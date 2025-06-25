from datetime import datetime
import os

import pytest
from selenium import webdriver
import logging
from core.pom import LoginPage


# 配置日志
def setup_logging():
    """设置日志格式和编码，解决中文乱码问题"""
    # 日志目录
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件名（带时间戳）
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # 配置日志基本参数
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            # 控制台处理器（默认编码为系统编码，可能需根据系统调整）
            logging.StreamHandler(),
            # 文件处理器，指定UTF-8编码
            logging.FileHandler(log_file, encoding="utf-8")
        ]
    )


setup_logging()
logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    driver.quit()


# 开始执行
def pytest_runtest_setup(item):
    logger.info(f'开始执行 {item.name}'.center(50, '-'))
    pass

# 结束执行
def pytest_runtest_teardown(item):
    logger.info(f'执行结束 {item.name}'.center(50, '-'))
    pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 如果找得到page就截图
    page = None
    if "driver" in item.fixturenames:
        driver = item.funcargs["driver"]
        page = LoginPage(driver)

    if report.when == 'call':
        o = report.outcome
        s = f"用例执行结束， 结果：【{report.outcome}】"
        if o == 'failed':
            logger.error(s)
        elif o == 'skip':
            logger.warning(s)
        else:
            logger.info(s)

        if page and hasattr(page, "screen_shot"):
            try:
                page.screen_shot(name=item.name)
                logger.info('页面截图完成')
            except Exception as e:
                logger.error(f'截图失败: {e}')
