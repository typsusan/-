from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import pyperclip
import time
from tkinter import messagebox
from chrome.get_chrome import get_chrome

def publish_to_51cto(account, password, title, content, tags, summary, log_callback=None):
    driver = get_chrome("51")
    try:
        log_callback("打开 51CTO 登录页面...")
        driver.get("https://home.51cto.com/index?from_service=blog&scene=login1&reback=https://blog.51cto.com/")
        wait = WebDriverWait(driver, 20)

        # 登录流程
        log_callback("正在点击密码登录按钮...")
        password_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='密码登录']")))
        password_login_button.click()

        log_callback("正在输入账号...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "loginform-username")))
        username_field.send_keys(account)

        log_callback("正在输入密码...")
        password_field = driver.find_element(By.ID, "loginform-password")
        password_field.send_keys(password)

        log_callback("正在点击登录按钮...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='登 录']")))
        login_button.click()
        log_callback("登录成功！")

        # 等待跳转到首页
        time.sleep(3)

        # Step 5: 跳转到写文章页面
        driver.get("https://blog.51cto.com/blogger/publish?old=1&newBloger=2")
        time.sleep(5)

        try:
            close_tip_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tip-close")))
            close_tip_button.click()
        except:
            log_callback("No 'tip-close' button found, continuing with the script.")

        time.sleep(5)

        # 输入标题
        log_callback("正在输入标题...")
        blog_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='title']")))
        blog_title.send_keys(title)

        time.sleep(3)

        # 输入正文
        log_callback("正在输入正文内容...")
        pyperclip.copy(content)  # 将内容复制到剪贴板
        blog_container = wait.until(EC.presence_of_element_located((By.ID, "container")))
        blog_container.click()
        blog_container.send_keys(Keys.CONTROL, 'v')  # Windows/Linux 中的 Ctrl+V

        time.sleep(5)

        try:
            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary') and .//span[text()='确 认']]")))
            confirm_button.click()
        except:
            log_callback("No '确认' button found, continuing without markdown confirmation.")

        time.sleep(3)

        # 发布文字调用除侧边栏
        publish_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'edit-submit') and .//span[text()='发布文章']]")))
        publish_button.click()
        time.sleep(3)

        # 输入标签
        log_callback("正在输入标签...")
        tag_field = wait.until(EC.visibility_of_element_located((By.ID, "tag-input")))
        tag_field.send_keys(tags)
        driver.execute_script("arguments[0].blur();", tag_field)  # 触发失去焦点

        # 输入文章摘要
        log_callback("正在输入文章摘要...")
        abstractData_field = wait.until(EC.presence_of_element_located((By.ID, "abstractData")))
        abstractData_field.send_keys(summary)

        # 发布文章
        log_callback("点击发布按钮...")
        final_publish_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='release' and @id='submitForm']")))
        final_publish_button.click()

        log_callback("文章已成功发布到 51CTO！")

        time.sleep(10)

    except Exception as e:
        log_callback(f"发布到 51CTO 失败: {e}")

    finally:
        driver.quit()
