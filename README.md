# Selenium-based-Testing-for-Qunar.com

基于selenium框架的“去哪儿网”测试项目

包括 BasePage封装，POM封装页面元素，数据驱动测试，验证码滑动，日志系统，报告生成等功能。

## allure 环境

报告生成需要allure库，而allure库需要java jdk环境，因此：

1. 进入[Java Downloads | Oracle](https://www.oracle.com/java/technologies/downloads/)下载对应的jdk安装包

2. 安装完成后，进入系统环境变量导入以下环境变量：

   ```
   JAVA_HOME：C:\xxx\Java\jdk-24
   系统Path变量添加：C:\xxx\Java\jdk-24\bin
   系统添加CLASSPATH：.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;
   ```

*注：java jdk最好安装在C盘，以获得更高的优先级*

3. 进入终端，运行以下命令验证java安装情况

   ```
   java --version
   ```

4. 解压项目根目录的 *allure-2.34.1.zip* 安装包到当前目录，并在系统环境变量添加环境变量：

   ```
   F:\xxx\xxx\allure-2.34.1\bin
   ```

5. 进入终端，验证allure安装情况：

   ```
   allure --version
   ```

   终端应该输出以下开头的提示信息：

   ```
   Usage: allure [options] [command] [command options]
   ```

## 运行

### 数据

在 *data/login_data.xlsx* 中，预置了一些测试用例，您可以自己添加更多的测试用例。

*目前仅仅包含登录功能的测试*

### 开始测试

运行 *main,.py* 文件，即可开始自动化测试，并在测试完成后自动跳出 allure 测试报告。

并在logs/log_{time}.log中查看测试情况。



## TODO

- 更多的测试功能
- 并行测试 xdist
- 分布式测试框架 Selenium Grid



