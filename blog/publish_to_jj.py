from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import pyperclip
import time
from tkinter import messagebox
from chrome.get_chrome import get_chrome

def publish_to_jj(account, password, title, content, tags, summary, log_callback=None):
    driver = get_chrome("jj")
    try:
        log_callback("打开 掘金 登录页面...")
        driver.get("https://juejin.cn/")
        wait = WebDriverWait(driver, 20)

        # 点击登录
        click_login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'login-button') and contains(text(), '登录')]"))
        )
        click_login_btn.click()

        time.sleep(3)

        # 点击密码登录
        pass_login_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "clickable"))
        )
        pass_login_btn.click()

        time.sleep(1)

        # 等待并定位手机号输入框
        log_callback("正在输入账号...")
        phone_input = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "account-input"))
        )
        phone_input.send_keys(account)  # 替换为您的手机号

        # 定位密码输入框
        log_callback("正在输入密码...")
        password_input = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "login-password"))
        )
        password_input.send_keys(password)  # 替换为您的密码

        # 定位并点击“登录”按钮
        log_callback("正在点击登录按钮...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-login"))
        )
        login_button.click()


        time.sleep(3)
        log_callback("登录成功！")


        # 等待跳转到首页
        time.sleep(3)

        # Step 5: 跳转到写文章页面
        driver.get("https://juejin.cn/editor/drafts/new?v=2")
        time.sleep(2)


        # 输入标题
        log_callback("正在输入标题...")
        blog_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title-input")))
        blog_title.send_keys(title)


        # 输入正文内容
        log_callback("正在输入正文内容...")

        # 使用 JavaScript 将内容输入到 CodeMirror 编辑器
        script = """
            const editor = document.querySelector('.CodeMirror').CodeMirror;
            editor.setValue(arguments[0]);
        """
        driver.execute_script(script, content)

        log_callback("正文内容输入完成")

        time.sleep(3)

        log_callback("点击发布 调用出弹窗")
        # 点击发布 调用出弹窗
        publish_pop_up_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'xitu-btn') and contains(text(), '发布')]"))
        )
        publish_pop_up_button.click()

        time.sleep(3)

        # 选择分类
        log_callback("选择分类....")
        frontend_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='item' and contains(text(), '阅读')]"))
        )
        frontend_option.click()

        time.sleep(2)

        # 点击标签
        log_callback("选择标签")
        dropdown_box = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "tag-input"))
        )
        dropdown_box.click()

        time.sleep(2)

        # 选择标签
        backend_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'byte-select-option') and contains(text(), '后端')]"))
        )
        backend_option.click()

        time.sleep(2)

        log_callback("输入文章摘要....")
        textarea = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "byte-input__textarea"))
        )
        textarea.send_keys(summary)

        #发布文章
        confirm_publish_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '确定并发布')]"))
        )
        confirm_publish_button.click()

        log_callback("文章已成功发布到掘金！")

        time.sleep(10)


    except Exception as e:
        log_callback(f"发布到 掘金 失败: {e}")
    finally:
        driver.quit()