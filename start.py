from datetime import datetime
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import messagebox, Toplevel, Entry, Button, PhotoImage
from threading import Thread
from blog.publish_to_51cto import publish_to_51cto
from blog.publish_to_bky import publish_to_bky
from blog.publish_to_js import publish_to_js
from blog.publish_to_jj import publish_to_jj
from blog.publish_to_csdn import publish_to_csdn
import winreg

class BlogPublisherApp:
    def __init__(self, root):
        self.root = root

        self.root.title("博客矩阵发布")
        self.root.geometry("1060x1410")
        self.root.resizable(False, False)

        self.icon = PhotoImage(file="app_icon.png")
        self.root.iconphoto(False, self.icon)

        self.center_window(self.root)
        global_padx = 15
        global_pady = 12

        style = ttk.Style()
        style.configure("Custom.TLabel", foreground="#fff", background="#2b3e50")

        self.create_text_input("博客标题:", "title", 0)
        self.create_text_input("标签:", "tag", 1)
        self.create_text_area("正文内容:", "content", 2, 12)
        self.create_text_area("文章摘要:", "summary", 3, 4)

        self.platforms = {
            "51CTO": ttk.BooleanVar(),
            "博客园": ttk.BooleanVar(),
            "简书": ttk.BooleanVar(),
            "掘金": ttk.BooleanVar(),
            "CSDN": ttk.BooleanVar()
        }
        self.platform_credentials = self.load_credentials_from_registry()
        self.lock_buttons = {}

        ttk.Label(root, text="发布平台:", bootstyle="secondary", style="Custom.TLabel").grid(row=4, column=0, padx=global_padx, pady=global_pady, sticky="ne")
        platform_frame = ttk.Frame(root)
        platform_frame.grid(row=4, column=1, padx=global_padx, pady=global_pady, sticky="w")

        for idx, (platform, var) in enumerate(self.platforms.items()):
            row_idx = idx + 4
            checkbox = ttk.Checkbutton(
                platform_frame, text=platform, variable=var,
                bootstyle="round-toggle",
                command=lambda p=platform, v=var: self.validate_platform_selection(p, v)
            )
            checkbox.grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")

            lock_icon = self.get_lock_icon(platform)
            config_button = ttk.Button(platform_frame, image=lock_icon, command=lambda p=platform: self.open_credential_popup(p), bootstyle="link")
            config_button.image = lock_icon
            config_button.grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
            self.lock_buttons[platform] = config_button

        self.publish_button = ttk.Button(root, text="确认发布", command=self.start_publish, bootstyle="success-outline")
        self.publish_button.grid(row=5, column=1, padx=global_padx, pady=global_pady, sticky="w")

        ttk.Label(root, text="发布日志:", bootstyle="secondary", style="Custom.TLabel").grid(row=6, column=0, padx=global_padx, pady=global_pady, sticky="ne")

        # 创建 Notebook 容器
        self.log_notebook = ttk.Notebook(root)
        self.log_notebook.grid(row=6, column=1, padx=global_padx, pady=global_pady, sticky="w")

        # 为每个平台创建日志标签页
        self.log_text_areas = {}
        for platform in self.platforms:
            frame = ttk.Frame(self.log_notebook)
            self.log_notebook.add(frame, text=platform)

            # 日志文本框和滚动条
            log_text = ttk.Text(frame, height=8, width=62, state="disabled", wrap="word")
            log_text.pack(side="left", fill="both", expand=True)
            scrollbar = ttk.Scrollbar(frame, command=log_text.yview)
            scrollbar.pack(side="right", fill="y")
            log_text.config(yscrollcommand=scrollbar.set)

            self.log_text_areas[platform] = log_text

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width() if window.winfo_width() > 1 else window.winfo_reqwidth()
        height = window.winfo_height() if window.winfo_height() > 1 else window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_text_input(self, label_text, attribute_name, row):
        ttk.Label(self.root, text=label_text, bootstyle="secondary", style="Custom.TLabel").grid(row=row, column=0, padx=15, pady=12, sticky="e")
        entry = ttk.Entry(self.root, bootstyle="info", width=62)
        entry.grid(row=row, column=1, padx=15, pady=12, sticky="w")
        setattr(self, f"{attribute_name}_entry", entry)

    def create_text_area(self, label_text, attribute_name, row, height):
        ttk.Label(self.root, text=label_text, bootstyle="secondary", style="Custom.TLabel").grid(row=row, column=0, padx=15, pady=12, sticky="ne")
        frame = ttk.Frame(self.root)
        frame.grid(row=row, column=1, padx=15, pady=12, sticky="w")
        text = ttk.Text(frame, height=height, width=60, wrap="word")
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")
        setattr(self, f"{attribute_name}_entry", text)

    def load_credentials_from_registry(self):
        credentials = {}
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\BlogPublisherApp", 0, winreg.KEY_READ) as key:
                for platform in ["51CTO", "博客园", "简书", "掘金", "CSDN"]:
                    try:
                        username = winreg.QueryValueEx(key, f"{platform}_username")[0]
                        password = winreg.QueryValueEx(key, f"{platform}_password")[0]
                        credentials[platform] = (username, password)
                    except FileNotFoundError:
                        credentials[platform] = ("", "")
        except FileNotFoundError:
            pass
        return credentials

    def save_credentials_to_registry(self, platform, username, password):
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\BlogPublisherApp")
            winreg.SetValueEx(key, f"{platform}_username", 0, winreg.REG_SZ, username)
            winreg.SetValueEx(key, f"{platform}_password", 0, winreg.REG_SZ, password)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Error saving to registry: {e}")

    def get_lock_icon(self, platform):
        if platform in self.platform_credentials and all(self.platform_credentials[platform]):
            icon_path = "lock_with_check.png"
        else:
            icon_path = "lock_with_cross.png"
        icon_image = Image.open(icon_path).resize((27, 27), Image.LANCZOS)
        return ImageTk.PhotoImage(icon_image)

    def update_lock_icon(self, platform):
        lock_icon = self.get_lock_icon(platform)
        button = self.lock_buttons[platform]
        button.config(image=lock_icon)
        button.image = lock_icon

    def open_credential_popup(self, platform):
        popup = Toplevel(self.root)
        popup.title(f"{platform} 账号设置")
        popup.geometry("650x200")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        self.center_window(popup)

        ttk.Label(popup, text=f"{platform}账号:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        account_entry = Entry(popup, width=30)
        account_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(popup, text=f"{platform}密码:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        password_entry = Entry(popup, show="*", width=30)
        password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        if platform in self.platform_credentials:
            account, password = self.platform_credentials[platform]
            account_entry.insert(0, account)
            password_entry.insert(0, password)

        Button(popup, text="保存", command=lambda: self.save_credentials(platform, account_entry.get(), password_entry.get(), popup)).grid(row=2, column=1, pady=20)

    def save_credentials(self, platform, username, password, popup):
        self.platform_credentials[platform] = (username, password)
        self.save_credentials_to_registry(platform, username, password)
        popup.destroy()
        self.update_lock_icon(platform)

    def validate_platform_selection(self, platform, var):
        if platform not in self.platform_credentials or not all(self.platform_credentials[platform]):
            var.set(False)
            messagebox.showwarning("提示", f"请先点击 {platform} 平台旁边的图标输入账号和密码。")

    def start_publish(self):
        selected_platforms = [platform for platform, var in self.platforms.items() if var.get()]
        if not selected_platforms:
            messagebox.showwarning("Warning", "请选择至少一个平台进行发布")
            return

        self.publish_button.grid_remove()
        for log_text in self.log_text_areas.values():
            log_text.config(state="normal")
            log_text.insert("end", "发布流程开始...\n")
            log_text.config(state="disabled")

        publish_thread = Thread(target=self.publish, args=(selected_platforms,))
        publish_thread.start()

    def update_log(self, platform, message):
        if platform in self.log_text_areas:
            log_text = self.log_text_areas[platform]
            log_text.config(state="normal")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"【{platform}】{timestamp} {message}\n"

            log_text.insert("end", formatted_message)
            log_text.see("end")
            log_text.config(state="disabled")

    def publish(self, selected_platforms):
        title = self.title_entry.get()
        content = self.content_entry.get("1.0", "end").strip()
        tags = self.tag_entry.get()
        summary = self.summary_entry.get("1.0", "end").strip()

        for platform in selected_platforms:
            account, password = self.platform_credentials.get(platform, ("", ""))
            if platform == "51CTO":
                publish_to_51cto(account, password, title, content, tags, summary, log_callback=lambda msg: self.update_log("51CTO", msg))
            if platform == "博客园":
                publish_to_bky(account, password, title, content, tags, summary, log_callback=lambda msg: self.update_log("博客园", msg))
            if platform == "简书":
                publish_to_js(account, password, title, content, tags, summary, log_callback=lambda msg: self.update_log("简书", msg))
            if platform == "掘金":
                publish_to_jj(account, password, title, content, tags, summary, log_callback=lambda msg: self.update_log("掘金", msg))
            if platform == "CSDN":
                publish_to_csdn(account, password, title, content, tags, summary, log_callback=lambda msg: self.update_log("CSDN", msg))

        self.publish_button.grid()

# 启动应用
root = ttk.Window(themename="superhero")
app = BlogPublisherApp(root)
root.mainloop()
