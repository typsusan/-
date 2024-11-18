from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import pyperclip
import time
from tkinter import messagebox
from chrome.get_chrome import get_chrome

def publish_to_js(account, password, title, content, tags, summary, log_callback=None):
    driver = get_chrome("js")
    try:
        log_callback("打开 简书 登录页面...")
        driver.get("https://www.jianshu.com/sign_in")
        wait = WebDriverWait(driver, 20)

        time.sleep(3)

        log_callback("正在输入账号...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "session_email_or_mobile_number")))
        username_field.send_keys(account)

        time.sleep(2)

        log_callback("正在输入密码...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
        password_field.send_keys(password)


        log_callback("正在点击登录按钮...")
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "sign-in-form-submit-btn")))
        login_button.click()

        time.sleep(3)
        log_callback("登录成功！")


        # 等待跳转到首页
        time.sleep(3)

        # Step 5: 跳转到写文章页面
        driver.get("https://www.jianshu.com/writer/")
        time.sleep(2)

        # 新建文章
        create_blog_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_1GsW5")))
        create_blog_button.click()

        time.sleep(2)


        # 输入标题
        log_callback("正在输入标题...")
        blog_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "_24i7u")))
        blog_title.clear()  # 清空已有内容
        time.sleep(1)
        blog_title.send_keys(title)


        # 输入正文
        log_callback("正在输入正文内容...")
        pyperclip.copy(content)  # 将内容复制到剪贴板
        blog_container = wait.until(EC.presence_of_element_located((By.ID, "arthur-editor")))
        blog_container.click()
        blog_container.send_keys(Keys.CONTROL, 'v')  # Windows/Linux 中的 Ctrl+V

        time.sleep(3)

        #发布文章
        publish_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@data-action='publicize']")))
        publish_button.click()


        log_callback("文章已成功发布到简书！")

        time.sleep(10)


    except Exception as e:
        log_callback(f"发布到 简书 失败: {e}")
    finally:
        driver.quit()