import os
import pytest

'''
对 去哪儿网 进行测试
'''

pytest.main()

# 运行完毕之后生成allure报告
os.system("allure serve .allure_results")