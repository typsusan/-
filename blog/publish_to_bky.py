from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import pyperclip
from tkinter import messagebox
import time
from chrome.get_chrome import get_chrome

def publish_to_bky(account, password, title, content, tags, summary, log_callback=None):
    driver = get_chrome("bky")
    try:
        log_callback("打开 博客园登录页面...")
        driver.get("https://account.cnblogs.com/signin?returnUrl=https:%2F%2Fwww.cnblogs.com%2F")
        wait = WebDriverWait(driver, 20)

        # 输入账号
        log_callback("正在输入账号...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        username_field.send_keys(account)

        # 输入密码
        log_callback("正在输入密码...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
        password_field.send_keys(password)

        # 点击登录按钮
        log_callback("正在点击登录按钮...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()=' 登录 ']]")))
        login_button.click()

        time.sleep(3)

        # 等待智能验证或其他验证处理
        log_callback("开始智能验证...")
        try:
            rect_mask = wait.until(EC.element_to_be_clickable((By.ID, "rectMask")))
            rect_mask.click()
            log_callback("使用方法1点击rectMask层成功")
        except:
            log_callback("方法1失败，跳过智能验证")

        # 等待跳转到首页
        log_callback("等待跳转到首页...")
        wait.until(EC.url_contains("https://www.cnblogs.com/"))

        # 跳转到写文章页面
        log_callback("跳转到写文章页面...")
        driver.get("https://i.cnblogs.com/articles/edit")

        # 输入标题
        log_callback("正在输入标题...")
        blog_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='post-title']")))
        blog_title.send_keys(title)

        # 输入正文内容
        log_callback("正在输入正文内容...")
        pyperclip.copy(content)
        blog_container = wait.until(EC.presence_of_element_located((By.ID, "md-editor")))
        blog_container.click()
        blog_container.send_keys(Keys.CONTROL, 'v')

        # 输入文章摘要
        log_callback("正在输入文章摘要...")
        abstract_field = wait.until(EC.presence_of_element_located((By.ID, "summary")))
        abstract_field.send_keys(summary)

        # 输入文章标签
        log_callback("正在输入文章标签...")
        tag_container = wait.until(
            EC.presence_of_element_located((By.XPATH, "//cnb-tag-input[.//label[text()='Tag 标签：']]"))
        )
        tag_input = tag_container.find_element(By.CSS_SELECTOR, "input.ant-select-selection-search-input")
        tag_input.send_keys(tags)
        tag_input.send_keys(Keys.TAB)

        time.sleep(3)

        # 发布文章
        log_callback("正在发布文章...")
        publish_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-el-locator='publishBtn']"))
        )
        publish_button.click()

        log_callback("文章已成功发布到博客园！")

        time.sleep(10)

    except Exception as e:
        log_callback(f"发布到博客园失败: {e}")

    finally:
        driver.quit()
