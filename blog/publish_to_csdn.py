from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import pyperclip
import time
from tkinter import messagebox
from chrome.get_chrome import get_chrome


def publish_to_csdn(account, password, title, content, tags, summary, log_callback=None):
    driver = get_chrome("csdn")
    try:
        log_callback("打开 CSDN 登录页面...")
        driver.get("https://passport.csdn.net/login?code=applets")
        wait = WebDriverWait(driver, 20)

        time.sleep(3)

        # 点击密码登录
        password_login_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '密码登录')]"))
        )
        password_login_option.click()

        time.sleep(3)

        # 等待并定位手机号输入框
        log_callback("正在输入账号...")
        username_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号/邮箱/用户名']"))
        )
        username_input.send_keys(account)

        # 定位密码输入框
        log_callback("正在输入密码...")
        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='密码']"))
        )
        password_input.send_keys(password)

        # 同意条款
        inform_title = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME,"icon-nocheck"))
        )
        inform_title.click()

        time.sleep(1)


        # 定位并点击“登录”按钮
        log_callback("正在点击登录按钮...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "base-button"))
        )
        login_button.click()

        time.sleep(3)
        log_callback("登录成功！")

        # 等待跳转到首页
        time.sleep(3)

        # Step 5: 跳转到写文章页面
        driver.get("https://editor.csdn.net/md/")
        time.sleep(2)

        # 输入标题
        log_callback("正在输入标题...")
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article-bar__title"))
        )
        title_input.clear()
        title_input.send_keys(title)

        # 输入正文内容
        log_callback("正在输入正文内容...")
        pyperclip.copy(content)
        content_input = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "editor__inner"))
        )
        content_input.click()
        content_input.clear()
        content_input.send_keys(Keys.CONTROL, 'v')

        time.sleep(5)

        log_callback("发布文章弹窗")
        # 点击发布文章弹窗
        publish_pop_up_btn = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-publish"))
        )
        publish_pop_up_btn.click()

        time.sleep(3)

        # 添加文章标签
        log_callback("正在输入文章标签...")
        tab_btn = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "tag__btn-tag"))
        )
        tab_btn.click()
        time.sleep(1)
        input_field = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-input__inner"))
        )
        input_field.clear()  # 清空内容（如果需要）
        input_field.send_keys(tags)  # 替换为您要输入的内容
        input_field.send_keys(Keys.RETURN)  # 模拟按下回车键

        time.sleep(2)

        # 文章摘要
        log_callback("正在输入文章摘要...")

        summary_input = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-textarea__inner"))
        )
        summary_input.send_keys(summary)

        time.sleep(2)

        close_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='mark_selection_box']//button[@title='关闭' and contains(@class, 'modal__close-button')]"))
        )
        close_button.click()

        time.sleep(2)

        log_callback("正在发布文章....")
        publish_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'modal__button-bar')]/button[contains(@class, 'btn-b-red') and contains(text(), '发布文章')]"
            ))
        )
        publish_button.click()

        log_callback("文章已成功发布到CSDN！")

        time.sleep(10)

    except Exception as e:
        log_callback(f"发布到 CSDN 失败: {e}")
    finally:
        driver.quit()
